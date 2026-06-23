#!/usr/bin/env python3
"""
db/src/main.py — Database deployment orchestrator for geopolitical_tracker.

Manages the full schema lifecycle in strict dependency order, ensuring that
each DDL layer is installed only after its prerequisites exist and torn down
before anything that depends on it is removed.

DEPLOY sequence
---------------
1. Schema creation          CREATE SCHEMA IF NOT EXISTS
2. PostgreSQL extensions    pg_trgm (trigram search), postgis (spatial data)
3. Native enum types        CREATE TYPE … AS ENUM for all ORM-mapped enums
4. ORM tables + indexes     Alembic versioned migrations (``upgrade head``)
5. Trigger functions        CREATE OR REPLACE FUNCTION update_tg()
6. Row-level triggers       BEFORE UPDATE trigger on every timestamped table

TEARDOWN sequence (reverse)
----------------------------
1. Row-level triggers       DROP TRIGGER IF EXISTS … ON …
2. Trigger functions        DROP FUNCTION … CASCADE
3. ORM tables               Alembic downgrade → base
4. Native enum types        DROP TYPE IF EXISTS … CASCADE
5. Extensions               Intentional no-op (see migrs/xts/xts.py)
6. Schema                   DROP SCHEMA IF EXISTS … CASCADE

Usage (from the project root)
------------------------------
    python -m src.main deploy
    python -m src.main teardown
    python -m src.main upgrade [<revision>]
    python -m src.main downgrade <revision>
    python -m src.main validate
    python -m src.main status

    Flags available on all commands:
        --skip-validation               Bypass pre-flight FK metadata check (development only)
        --yes / -y                      Suppress interactive confirmation for destructive ops
        --echo-sql                      Echo every SQL statement to stdout
        --phase {"a","b","c","all"}     Allows partial deployment for development or debugging.

Prerequisites
-------------
- Python ≥ 3.10  (structural pattern matching is used in the dispatch block)
- PostgreSQL ≥ 14 (CREATE OR REPLACE TRIGGER syntax)
- PostGIS and pg_trgm available as installable extensions on the target server
- DB_URL set in db/src/config/.env or as an environment variable
- All FK references in the ORM models use plural table names matching
  TablenameMixin.__tablename__ output; _validate_metadata() will fail fast
  if any mismatch exists (see review: _fk_ref/_secondary_ref naming fix)

Known dependencies to address before first deploy
--------------------------------------------------
- db/migrs/env/env.py must contain the mode-dispatch block at module level:
      if context.is_offline_mode():
          run_migrations_offline()
      else:
          run_migrations_online()
- _fk_ref() and _secondary_ref() in db/utils/funcs/funcs.py must pluralise
  their table name argument to match TablenameMixin output.
- _get_tbl() must filter to tables possessing an updated_at column before
  the trigger migration is run; see db/utils/funcs/funcs.py review note.
"""
from __future__ import annotations
import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Callable, NoReturn

_HERE: Path = Path(__file__).resolve()
_SRC_DIR: Path = _HERE.parent 
_PROJECT_ROOT: Path = _SRC_DIR.parent 

if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

if sys.version_info < (3, 10):
    sys.exit(
        f"Python 3.10 or later is required (found {sys.version}). "
        "Upgrade your interpreter or virtual environment."
    )

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.pool import NullPool

from src.config.config import Settings, get_settings
from mdls.base.base import Base
from utils.utils.metadata import _validate_metadata, _get_schema
from utils.utils.sec import sec_dsn
from migrs.xts import xts as _xts
from migrs.enums import enums as _enums_mig
from migrs.funcs import funcs as _funcs_mig
from migrs.trgs import trgs as _trgs_mig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    stream=sys.stderr
)
_log: logging.Logger = logging.getLogger("deploy")

_ALEMBIC_INI: Path = _SRC_DIR / "alembic.ini"
_CONFIRM_PHRASE: str = "CONFIRM"

def _die(message: str, code: int = 1) -> NoReturn:
    """
    Log a critical error message and terminate the process with the given
    exit code.

    This is a convenience wrapper that logs the message at the `CRITICAL`
    level and then calls `sys.exit(code)`. It is used throughout the
    orchestrator to halt execution cleanly when a fatal condition is
    encountered (e.g., missing configuration, validation failure, database
    unreachable). The use of `NoReturn` in the return type annotation
    signals that this function never returns normally.

    Parameters:
        message (str): The error message to log. It will be prefixed with
            a timestamp and severity level by the logging system.
        code (int, optional): The exit status code to return to the calling
            process. Defaults to `1` (general error). Use `0` only for
            deliberate non‑error exits (but this function is typically
            used for errors).

    Returns:
        NoReturn: This function does not return; it terminates the process.

    Notes:
        - All unhandled exceptions in `main()` are caught and logged, but
          `_die` is used for explicit, known failure points.
        - The function is called before and during database operations to
          provide clear feedback to the operator or CI/CD system.

    Example:
        >>> if not _ALEMBIC_INI.is_file():
        ...     _die("alembic.ini not found.")
    """
    _log.critical(message)
    sys.exit(code)

def _require_confirmation(action: str) -> None:
    """
    Interactively demand that the operator type a specific confirmation phrase
    before a destructive command proceeds.

    This function is used as a safeguard for operations like `teardown` that
    permanently remove data. It logs a warning describing the action and the
    affected schema, then prompts the user to type the exact phrase
    `"CONFIRM"`. If the input matches, the function returns normally and the
    destructive operation continues. If the input is anything else (including
    EOF or keyboard interrupt), the program exits with code `0` (meaning the
    operator chose to abort) without executing the destructive operation.

    Parameters:
        action (str): A human‑readable description of the destructive
            operation (e.g., `"teardown"`). This is used in the warning
            message.

    Returns:
        None: If the user confirms successfully. Otherwise, the process
            terminates.

    Raises:
        SystemExit: When the user aborts (response does not match, or no
            input is provided). The exit code is `0` to indicate a deliberate
            cancellation, not an error.

    Notes:
        - The confirmation phrase is stored in the module constant
          `_CONFIRM_PHRASE` (currently `"CONFIRM"`).
        - This function is only called when the `--yes`/`-y` flag is **not**
          supplied. In non‑interactive environments, the flag should be used
          to skip the prompt.
        - The schema name is obtained via `_get_schema(Base.metadata)` and
          displayed in the warning.

    Example:
        >>> _require_confirmation("full schema reset")
        # Logs warning and prompts user.
    """
    _log.warning(
        "⚠  DESTRUCTIVE OPERATION: %s",
        action.upper()
    )
    _log.warning(
        "⚠  All data in schema '%s' will be permanently lost.", _get_schema(Base.metadata)
    )
    try:
        response: str = input(
            f"\n  Type exactly '{_CONFIRM_PHRASE}' to proceed, "
            "anything else to abort: "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        _log.info("Aborted (no input).")
        sys.exit(0)

    if response != _CONFIRM_PHRASE:
        _log.info("Aborted by operator.")
        sys.exit(0)

def _alembic_cfg() -> AlembicConfig:
    """
    Build and return an Alembic `Config` object sourced from `alembic.ini`.

    This function locates the `alembic.ini` file (expected at
    `db/src/alembic.ini` relative to the project root) and loads it into
    an Alembic `Config` object. It then injects the database URL and a
    `connect_args` option to set the PostgreSQL `search_path` to the
    application schema (plus `public`) so that all Alembic operations
    execute in the correct schema context.

    The injection is done explicitly as a string to work around a known
    type‑coercion issue in the `env.py` file where `settings.DB_URL` is
    a `PostgresDsn` object that may not convert cleanly to a string when
    passed to `config.set_main_option()`. By setting the URL here before
    Alembic loads `env.py`, we ensure the value is correctly typed.

    Returns:
        AlembicConfig: A fully configured Alembic configuration object,
            ready to be passed to Alembic commands (`upgrade`, `downgrade`,
            `current`, etc.).

    Raises:
        SystemExit: If the `alembic.ini` file does not exist at the expected
            location, the function calls `_die()` and terminates.

    Notes:
        - The `search_path` is set in two places: in the URL as a query
          parameter (`options=-c%20search_path=...`) and in the
          `sqlalchemy.connect_args` option. The latter is the recommended
          way for SQLAlchemy 2.x.
        - This function is called by every Alembic‑related command (`upgrade`,
          `downgrade`, `status`) and by `deploy`/`teardown` when invoking
          Alembic.
    """
    if not _ALEMBIC_INI.is_file():
        _die(
            f"alembic.ini not found at expected path: {_ALEMBIC_INI}\n"
            "Ensure alembic.ini exists at db/src/alembic.ini."
        )
    _settings: Settings = get_settings()
    url: str = str(_settings.DB_URL)
    schema: str = _settings.DB_SCHEMA
    cfg: AlembicConfig = AlembicConfig(str(_ALEMBIC_INI))
    
    if "options" not in url and "search_path" not in url:
        url += f"options=-c%20search_path={schema},public"
    cfg.set_main_option("sqlalchemy.connect_args", '{"options": "-c search_path=...}"}')
    return cfg

def _make_engine(*, echo: bool = False) -> Engine:
    """
    Return a fully configured SQLAlchemy `Engine` for the target database.

    The engine is created using the application settings (`DB_URL` and
    `DB_SCHEMA`) and configured with:
        - `poolclass=NullPool`: Disables connection pooling to avoid
          lingering connections after the engine is disposed.
        - `connect_args={"options": f"-c search_path={schema},public"}`:
          Sets the PostgreSQL `search_path` so that all operations (DDL,
          queries) default to the application schema.
        - `echo=echo`: Controls SQL logging. The `echo` parameter is
          typically set via the `--echo-sql` flag or automatically when
          the environment is `development`.

    The engine uses SQLAlchemy 2.x future‑style API and is suitable for
    both DDL and DML operations.

    Parameters:
        echo (bool, optional): If `True`, all SQL statements emitted by
            the engine are logged to `stdout`. Defaults to `False`. The
            caller typically passes `args.echo_sql or (settings.ENV == "development")`.

    Returns:
        Engine: A SQLAlchemy `Engine` instance ready for use.

    Notes:
        - This engine is used for the schema management steps that do not
          go through Alembic (schema creation, extension/enum/trigger
          migrations). Alembic uses its own engine from the configuration.
        - The engine should be disposed after use (as done in `finally` of
          `main()`).
    """
    _settings: Settings = get_settings()
    schema: str = _settings.DB_SCHEMA
    return create_engine(
        str(_settings.DB_URL),
        echo=echo,
        poolclass=NullPool,
        connect_args={"options": f"-c search_path={schema},public"}
    )

def _probe_connection(engine: Engine) -> None:
    """
    Verify database reachability by executing a trivial `SELECT 1` query.

    This function attempts to connect to the database using the provided
    engine and runs a simple query. If the connection succeeds, it logs a
    success message. If it fails with an `OperationalError` (or any other
    database‑related exception), it calls `_die()` with a clear error
    message explaining possible causes.

    This pre‑flight check is run before any migration or deployment step to
    avoid cryptic driver‑level exceptions that might be difficult to debug.
    It also logs the redacted DSN (via `sec_dsn()`) for auditing.

    Parameters:
        engine (Engine): A SQLAlchemy engine to test connectivity.

    Raises:
        SystemExit: If the connection fails, the function terminates with
            an error message and exit code `1`.

    Notes:
        - The function uses `sec_dsn()` to redact sensitive credentials in
          the log output.
        - The error message includes suggestions to check the URL, network
          access, and server status.
        - This function is called after `_preflight()` and before any
          destructive operations.
    """
    _settings: Settings = get_settings()
    _log.info(
        "Verifying database connectivity …\n"
        f"DB_URL = %s", sec_dsn(str(_settings.DB_URL))
    )
            
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as exc:
        _die(
            f"Cannot connect to database url.\n"
            f"Verify DB_URL, network access, and that the PostgreSQL server is running.\n"
            f"Driver error: {exc}"
        )
    _log.info("Database connection OK.")

def _create_schema(conn: Connection, schema: str) -> None:
    """
    Create the target database schema if it does not already exist.

    This is a simple wrapper around SQLAlchemy's `CreateSchema` construct
    with `if_not_exists=True`, making the operation idempotent. It is safe
    to call repeatedly; it will log that the schema is present after creation
    or if it already exists.

    Parameters:
        conn (Connection): An active SQLAlchemy connection (inside a
            transaction if needed).
        schema (str): The name of the schema to create.

    Notes:
        - This function is used in the Phase A of `deploy()`.
        - The `if_not_exists` clause is supported by PostgreSQL 9.6+.
        - The schema creation is performed within the caller's transaction.
    """
    conn.execute(CreateSchema(schema, if_not_exists=True))
    _log.info("Schema '%s' is present.", schema)

def _drop_schema(conn: Connection, schema: str) -> None:
    """
    Drop the target schema and all its contained objects via `CASCADE`.

    This is the final, destructive step of `teardown()`. It uses SQLAlchemy's
    `DropSchema` with `if_exists=True` and `cascade=True` to remove the
    schema and every object within it (tables, views, sequences, functions,
    types, etc.) in a single atomic operation. The `CASCADE` option ensures
    that dependencies are automatically handled.

    Parameters:
        conn (Connection): An active SQLAlchemy connection (must be inside
            a transaction to allow rollback on failure).
        schema (str): The name of the schema to drop.

    Notes:
        - This operation is irreversible; all data in the schema is lost.
        - The function is called after all other objects (triggers, functions,
          tables, enums) have already been dropped, so the `CASCADE` serves
          as a safety net to clean up any remaining references.
        - In `teardown()`, this is executed inside a transaction, but the
          transaction is committed after the full phase, making the drop
          permanent.
    """

    conn.execute(
        DropSchema(
            schema, 
            if_exists=True, 
            cascade=True
        )
    )
    _log.info("Schema '%s' dropped (CASCADE).", schema)
    
def _run_in_alembic_context(
    conn: Connection,
    fn: Callable[[], None],
    label: str,
) -> None:
    """
    Execute a migration callable inside a properly wired Alembic
    `Operations` context.

    This function is the glue that allows migration modules (e.g.,
    `migrs.enums.enums`, `migrs.funcs.funcs`) to use `from alembic import op`
    and have `op.execute()`, `op.get_bind()`, etc., work correctly. It
    configures a `MigrationContext` against the provided connection and
    activates it as the current context using `Operations.context()`. Inside
    this context, the module‑level `op` proxy will delegate to the
    operations of this context.

    The connection supplied must already be inside an open transaction
    (the caller should use `engine.begin()` or `conn.begin()`) so that the
    operations performed by `fn` are part of a transactional unit.

    Parameters:
        conn (Connection): An active SQLAlchemy connection, already within
            a transaction.
        fn (Callable[[], None]): The migration function to execute
            (typically `upgrade()` or `downgrade()` from a migration module).
        label (str): A human‑readable description of the step for logging
            (e.g., `"native PostgreSQL enum types"`).

    Raises:
        Any exception raised by `fn()` will propagate up and be handled by
        the caller (which typically catches `SQLAlchemyError`).

    Notes:
        - This function is used in `deploy()` and `teardown()` for the
          non‑Alembic migrations (extensions, enums, functions, triggers).
        - It logs a start and completion message using the provided `label`.
        - The context is active only for the duration of `fn()`; after it
          returns, the context is reset to its previous state.
        - This function does **not** commit or roll back the transaction;
          that is the responsibility of the caller.
    """
    _log.info("▶  %s", label)
    migration_ctx: MigrationContext = MigrationContext.configure(conn)
    with Operations.context(migration_ctx):
        fn()
    _log.info("✓  %s", label)

def _preflight(*, skip_validation: bool = False) -> None:
    """
    Validate ORM metadata foreign key integrity before any database operation.

    This function calls `_validate_metadata(Base.metadata)` to check that
    every foreign key constraint defined in the ORM models references an
    existing table and column within the same metadata. This catches naming
    mismatches (e.g., singular vs. plural table names in `_fk_ref` and
    `_secondary_ref`) early.

    If `skip_validation` is `True`, the validation is bypassed with a warning
    log. This flag should **only** be used during active model development
    when the naming conventions are still being refactored. It must never
    be used in CI/CD or production deployments.

    If validation fails, `_validate_metadata()` raises a `ValueError` with
    a list of all failing constraints. This function catches that exception
    and calls `_die()` with the detailed error list, forcing the operator
    to fix all issues before proceeding.

    Parameters:
        skip_validation (bool, optional): If `True`, skips the validation
            and logs a warning. Defaults to `False`.

    Raises:
        SystemExit: If validation fails and `skip_validation` is `False`.

    Notes:
        - This is a pre‑flight check that runs **before** any database
          connection is attempted (except when the command is `validate`,
          which runs only this check).
        - The validation uses `_resolve_tbl()` from `metadata.py`, which
          handles both qualified and unqualified table names.
        - If validation passes, a success message is logged.
    """
    if skip_validation:
        _log.warning(
            "Pre-flight metadata validation SKIPPED (--skip-validation). "
            "Never use this flag in production."
        )
        return

    _log.info("Pre-flight: validating ORM metadata FK references …")
    try:
        _validate_metadata(Base.metadata)
    except ValueError as exc:
        _die(
            "Pre-flight FAILED — ORM metadata contains unresolvable FK references.\n"
            "Fix all issues listed below before retrying deploy.\n\n"
            f"{exc}"
        )
    _log.info("Pre-flight: all FK references resolved. ✓")

def deploy(engine: Engine, phase: str = "all") -> None:
    """
    Execute the full forward deployment sequence in strict dependency order.

    The sequence is divided into three transactional phases to match natural
    dependency boundaries. Steps 1–3 (schema, extensions, enum types) must
    complete before Alembic can reference native PostgreSQL enum types in
    table DDL. Steps 5–6 (trigger function, triggers) must run after the
    ORM tables exist because CREATE TRIGGER references a specific table.

    Phase A — Schema, extensions, enum types (single transaction)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Wrapped in a single engine.begin() so that if extension installation or
    enum type creation fails, the schema is not left in a partially-initialised
    state. The CREATE SCHEMA IF NOT EXISTS and CREATE EXTENSION IF NOT EXISTS
    clauses are idempotent, making the entire phase safe to re-run.
    
    Phase B — ORM tables and indexes (Alembic manages its own transaction)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    alembic_command.upgrade() creates its own engine and connection from the
    configured URL. It must NOT share the Phase A connection because Alembic
    handles its own transaction boundaries around each revision. Alembic
    records each successfully applied revision in the alembic_version table,
    making this phase idempotent across repeated invocations.
    
    Phase C — Trigger function and triggers (single transaction)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Both objects depend on the ORM tables existing (CREATE TRIGGER references
    specific tables). Grouping them in one transaction ensures that neither a
    partially-installed trigger function nor a set of triggers without their
    backing function can be left in place if the phase fails partway through.
    """
    schema: str = _get_schema(Base.metadata)
    _log.info("━━━  DEPLOY  PHASE A begin  ━━━  target schema: '%s'", schema)
    
    if phase in ("a", "all"):
        _log.info("Phase A: schema · extensions · enum types")
        try:
            with engine.begin() as conn:
                _create_schema(conn, schema)
                _run_in_alembic_context(
                    conn,
                    _xts.upgrade,
                    "extensions (pg_trgm, postgis)"
                )
                _run_in_alembic_context(
                    conn,
                    _enums_mig.upgrade,
                    "native PostgreSQL enum types"
                )
        except SQLAlchemyError as exc:
            _die(f"DEPLOY failed at Phase A (schema/extensions/enums): {exc}")
    
    if phase in ("b", "all"):
        _log.info("━━━  DEPLOY  PHASE B begin  ━━━  target schema: '%s'", schema)
        try:
            with engine.connect() as conn:
                res: Any | None = conn.execute(
                    text("SELECT 1 FROM information_schema.schemata WHERE schema_name = :s"),
                    {"s": schema}
                ).scalar()
                if not res:
                    _die(f"Schema does not exist. Run Phase A (deploy_a) first.")
        except SQLAlchemyError as exc:
            _die(f"Failed to verify schema existence: {exc}")
        
        _log.info("Phase B: ORM tables and indexes (alembic upgrade head)")
        try:
            alembic_command.upgrade(_alembic_cfg(), "head")
        except Exception as exc:
            _die(f"DEPLOY failed at Phase B (Alembic table migrations): {exc}")
        _log.info("✓  Phase B complete.")
    
    if phase in ("c", "all"):
        _log.info("━━━  DEPLOY  PHASE C begin  ━━━  target schema: '%s'", schema)
        try: 
            with engine.connect() as conn:
                res: Any | None = conn.execute(
                    text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = :schema AND table_name = 'alembic_version')"),
                    {"schema": schema}
                ).scalar()
                if not res:
                    _die(f"Tables do not exist. Run Phase B (deploy_b) first.")
        except SQLAlchemyError as exc:
            _die(f"Failed to verify tables existence:  {exc}")
        
        _log.info("Phase C: trigger function · row-level triggers")
        try:
            with engine.begin() as conn:
                _run_in_alembic_context(
                    conn,
                    _funcs_mig.upgrade,
                    "trigger function (update_tg)"
                )
                _run_in_alembic_context(
                    conn,
                    _trgs_mig.upgrade,
                    "BEFORE UPDATE triggers on timestamped tables"
                )
        except SQLAlchemyError as exc:
            _die(f"DEPLOY failed at Phase C (trigger function/triggers): {exc}")

    _log.info("━━━  DEPLOY complete  ━━━")

def teardown(engine: Engine) -> None:
    """
    Execute the full reverse teardown sequence in strict reverse dependency order.

    The inverse of deploy(). Each phase removes objects that were created in
    the corresponding deploy phase, in reverse order. Errors in an early phase
    are fatal — the teardown halts rather than proceeding with an inconsistent
    intermediate state that could be harder to recover from than a clean failure.

    Phase A — Triggers and trigger function (single transaction)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    DROP TRIGGER IF EXISTS and DROP FUNCTION IF EXISTS are both conditional, so
    this phase is safe to re-run even if a previous teardown left the schema in
    an intermediate state.

    Phase B — ORM tables (Alembic manages its own transaction)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    alembic_command.downgrade("base") reverses every applied revision. On a
    schema that has already been fully downgraded, this is a safe no-op.

    Phase C — Enum types, extensions, schema (single transaction)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Enum types are dropped with CASCADE to release any remaining type references.
    Extensions are intentionally not dropped (xts.downgrade is a no-op) because
    dropping postgis CASCADE would destroy geography columns in any other schema
    sharing the same PostgreSQL cluster. The final DROP SCHEMA … CASCADE removes
    all remaining objects in one atomic operation.
    """
    schema: str = _get_schema(Base.metadata)
    _log.info("━━━  TEARDOWN  begin  ━━━  target schema: '%s'", schema)

    _log.info("Phase A: row-level triggers · trigger function")
    try:
        with engine.begin() as conn:
            _run_in_alembic_context(
                conn,
                _trgs_mig.downgrade,
                "BEFORE UPDATE triggers [down]"
            )
            _run_in_alembic_context(
                conn,
                _funcs_mig.downgrade,
                "trigger function (update_tg) [down]"
            )
    except SQLAlchemyError as exc:
        _die(f"TEARDOWN failed at Phase A (trigger removal): {exc}")

    _log.info("Phase B: ORM tables (alembic downgrade base)")
    try:
        alembic_command.downgrade(_alembic_cfg(), "base")
    except Exception as exc:
        _die(f"TEARDOWN failed at Phase B (Alembic table downgrade): {exc}")
    _log.info("✓  Phase B complete.")

    _log.info("Phase C: enum types · extensions [no-op] · schema drop")
    try:
        with engine.begin() as conn:
            _run_in_alembic_context(
                conn,
                _enums_mig.downgrade,
                "native PostgreSQL enum types [down]"
            )
            _run_in_alembic_context(
                conn,
                _xts.downgrade,
                "extensions [down] (intentional no-op)"
            )
            _drop_schema(conn, schema)
    except SQLAlchemyError as exc:
        _die(f"TEARDOWN failed at Phase C (enum/schema removal): {exc}")

    _log.info("━━━  TEARDOWN complete  ━━━")

def alembic_upgrade(revision: str = "head") -> None:
    """
    Advance ORM table migrations to the specified Alembic revision.

    This command **only** runs Alembic‑managed table migrations. It does not
    touch extensions, enum types, trigger functions, or triggers. Use the
    full `deploy` command for the complete schema setup.

    The operation is idempotent: if the database is already at or beyond the
    target revision, Alembic will do nothing.

    Parameters:
        revision (str, optional): The target Alembic revision identifier.
            Can be a full revision hash, a relative specifier like `+1`, or
            `"head"` (latest). Defaults to `"head"`.

    Raises:
        SystemExit: If Alembic raises an exception (e.g., missing revision),
            the function calls `_die()`.

    Notes:
        - This function is called by the `upgrade` CLI command.
        - It uses `_alembic_cfg()` to obtain the configuration.
        - Logs the revision being applied and success/failure.
    """
    _log.info("alembic upgrade → '%s'", revision)
    alembic_command.upgrade(_alembic_cfg(), revision)
    _log.info("✓  alembic upgrade complete.")

def alembic_downgrade(revision: str) -> None:
    """
    Revert ORM table migrations to a specified Alembic revision.

    This command **only** reverts Alembic‑managed table migrations. It does
    not touch trigger functions, triggers, enum types, or extensions. Use
    the full `teardown` command to remove everything.

    The target revision can be:
        - A specific revision hash or alias (e.g., `"abc123"`).
        - A relative specifier like `-1` or `-2` (steps back).
        - `"base"` to revert all migrations (empty schema, but only for
          Alembic‑managed tables).

    This operation is destructive to table data; all changes applied after
    the target revision will be reversed.

    Parameters:
        revision (str): The target Alembic revision identifier. This
            parameter is required.

    Raises:
        SystemExit: If Alembic raises an exception (e.g., invalid revision),
            the function calls `_die()`.

    Notes:
        - This function is called by the `downgrade` CLI command.
        - It uses `_alembic_cfg()` to obtain the configuration.
        - The downgrade is not automatically reversible; a subsequent
          upgrade would be needed to restore the schema.
    """
    _log.info("alembic downgrade → '%s'", revision)
    alembic_command.downgrade(_alembic_cfg(), revision)
    _log.info("✓  alembic downgrade complete.")

def alembic_status() -> None:
    """
    Print the current applied Alembic revision and any unapplied heads.

    This command connects to the database using the Alembic configuration
    and displays:
        - The current revision (the one recorded in `alembic_version`).
        - All available head revisions (including those not yet applied).
        - Verbose output showing the migration path.

    It is a read‑only operation and safe to run at any time without modifying
    the schema.

    Raises:
        SystemExit: If Alembic fails to connect or retrieve the revision,
            the function calls `_die()`.

    Notes:
        - This function is called by the `status` CLI command.
        - It uses `alembic_command.current()` and `alembic_command.heads()`.
        - The output is printed to stdout; the logs go to stderr.
    """
    cfg: AlembicConfig = _alembic_cfg()
    _log.info("Current applied revision:")
    alembic_command.current(cfg, verbose=True)
    _log.info("Available heads (unapplied revisions would appear here):")
    alembic_command.heads(cfg, verbose=True)

def validate_only() -> None:
    """
    Run metadata FK validation without any database connection.

    This is a standalone validation that checks the integrity of all
    foreign key references in the ORM metadata. It is useful for CI/CD
    pipelines to catch naming mismatches or broken references before
    attempting a deployment.

    The function calls `_validate_metadata(Base.metadata)` and logs success
    or exits with an error if validation fails.

    Raises:
        SystemExit: If validation fails, the function calls `_die()` with
            the list of errors.

    Notes:
        - This function is called by the `validate` CLI command.
        - It does **not** require a database connection, so it runs quickly
          and can be used in offline environments.
        - The validation uses the same logic as `_preflight()` with
          `skip_validation=False`.
    """
    _log.info("Metadata-only validation (no database access) …")
    try:
        _validate_metadata(Base.metadata)
    except ValueError as exc:
        _die(f"Metadata validation failed:\n{exc}")
    _log.info("✓  All FK references resolved correctly.")

def _build_parser() -> argparse.ArgumentParser:
    """
    Construct and configure the command‑line argument parser for the
    deployment orchestrator.

    This function defines all subcommands (`deploy`, `teardown`, `upgrade`,
    `downgrade`, `validate`, `status`) and their respective options and
    arguments. It also sets up global flags (`--skip-validation`, `--yes`,
    `--echo-sql`, `--phase`).

    Returns:
        argparse.ArgumentParser: A fully configured parser ready to parse
            command‑line arguments.

    Notes:
        - The parser uses `RawDescriptionHelpFormatter` to preserve the
          multi‑line description in the help text.
        - Subcommands are required (`dest="command"`, `required=True`).
        - The `--phase` option is only meaningful for the `deploy` command,
          but it is defined at the top level for simplicity; other commands
          ignore it.
        - The parser is called in `main()` to parse `sys.argv`.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src.main",
        description=(
            "Geopolitical Tracker — database deployment orchestrator.\n\n"
            "Commands\n"
            "--------\n"
            "  deploy     Full forward deployment (idempotent).\n"
            "             schema → extensions → enums → tables → functions → triggers\n\n"
            "  teardown   DESTRUCTIVE: removes all schema objects and data.\n"
            "             triggers → functions → tables → enums → schema DROP\n\n"
            "  upgrade    Advance Alembic ORM-table migrations only.\n\n"
            "  downgrade  Revert Alembic ORM-table migrations to a revision.\n"
            "             Use 'base' to remove all versioned migrations.\n\n"
            "  validate   Check ORM metadata FK integrity (no DB access required).\n\n"
            "  status     Show current Alembic revision and any pending heads.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        default=False,
        help=(
            "Bypass pre-flight ORM metadata FK validation. "
            "Use ONLY during development when model FK names are actively being "
            "refactored. Never pass this flag in CI/CD or production pipelines."
        )
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        default=False,
        help=(
            "Skip interactive confirmation prompts for destructive operations "
            "(teardown). Intended for non-interactive CI/CD environments. "
            "Exercise extreme caution when using against production databases."
        )
    )
    parser.add_argument(
        "--echo-sql",
        action="store_true",
        default=False,
        help=(
            "Echo all SQL statements to stdout. Overrides the automatic echo "
            "behaviour (which echoes when settings.ENV == 'development'). "
            "Useful for auditing the exact DDL emitted during a deployment."
        )
    )
    parser.add_argument(
        "--phase",
        choices=["a", "b", "c", "all"],
        default="all",
        help="Run only a specific deployment phase (a, b, c) or all (default)."
    )

    sub: argparse._SubParsersAction = parser.add_subparsers(dest="command", required=True)

    sub.add_parser(
        "deploy",
        help="Full forward deployment: schema → extensions → enums → tables → triggers."
    )

    sub.add_parser(
        "teardown",
        help=(
            "DESTRUCTIVE — drops all schema objects. "
            "Requires interactive confirmation unless --yes is supplied."
        )
    )

    upgrade_p: argparse.ArgumentParser = sub.add_parser(
        "upgrade",
        help="Run Alembic ORM-table migrations to a target revision."
    )
    upgrade_p.add_argument(
        "revision",
        nargs="?",
        default="head",
        metavar="REVISION",
        help=(
            "Alembic revision identifier or branch label. "
            "Defaults to 'head' (latest). Accepts partial revision IDs."
        )
    )

    downgrade_p: argparse.ArgumentParser = sub.add_parser(
        "downgrade",
        help="Revert Alembic ORM-table migrations to a target revision."
    )
    downgrade_p.add_argument(
        "revision",
        metavar="REVISION",
        help=(
            "Alembic revision identifier, relative specifier (e.g. -1, -2), "
            "or 'base' to remove all versioned table DDL."
        )
    )

    sub.add_parser(
        "validate",
        help=(
            "Validate ORM metadata FK references without connecting to the database. "
            "Safe to run in any environment at any time."
        )
    )

    sub.add_parser(
        "status",
        help="Print the current Alembic revision and any unapplied migration heads."
    )

    return parser

def main() -> None:
    """
    CLI entry point for the database deployment orchestrator.

    This function performs the following steps in order:
        1. Parses command‑line arguments via `_build_parser()`.
        2. Retrieves application settings (for logging and DB URL).
        3. If the command is not `validate`, runs `_preflight()` (metadata
           validation).
        4. If the command is `teardown` and `--yes` is **not** supplied,
           calls `_require_confirmation()` to ask for interactive
           confirmation.
        5. Builds a database engine using `_make_engine()` (respecting
           `--echo-sql` and development environment).
        6. Probes database connectivity with `_probe_connection()`.
        7. Dispatches the command to the appropriate handler function
           (`deploy`, `teardown`, `alembic_upgrade`, `alembic_downgrade`,
           `alembic_status`, or `validate_only`).
        8. Catches any unhandled exceptions, logs them, and exits with
           code `1`.
        9. Ensures the engine is disposed in a `finally` block.

    The function exits with code `0` on success, code `1` on error, or
    code `0` on deliberate abort (e.g., confirmation failed).

    Raises:
        SystemExit: Raised via `_die()` for fatal errors, or via `sys.exit(0)`
            for successful completion or user abortion.

    Notes:
        - The `match` statement (Python 3.10+) is used for command dispatch.
        - The `--skip-validation` flag is respected only if the command is
          not `validate`; the `validate` command always runs validation.
        - The engine is disposed after the command completes to release
          connections.
        - All exceptions that reach `main()` are caught and logged with full
          traceback before exiting.
    """
    parser: argparse.ArgumentParser = _build_parser()
    args: argparse.Namespace = parser.parse_args()
    
    _settings: Settings = get_settings()
    _log.info("Database target: %s", sec_dsn(str(_settings.DB_URL)))
    
    if args.command != "validate":
        _preflight(skip_validation=args.skip_validation)

    if args.command == "validate":
        validate_only()
        return

    if args.command == "teardown" and not args.yes:
        _require_confirmation("teardown")

    echo_sql: bool = args.echo_sql or (_settings.ENV == "development")
    engine: Engine = _make_engine(echo=echo_sql)
    _probe_connection(engine)

    try:
        match args.command:
            case "deploy":
                deploy(engine, phase=args.phase)
            case "teardown":
                teardown(engine)
            case "upgrade":
                alembic_upgrade(args.revision)
            case "downgrade":
                alembic_downgrade(args.revision)
            case "status":
                alembic_status()
            case _:
                _die(f"Unrecognised command: '{args.command}'. Run with --help.")
    except SystemExit:
        raise
    except Exception as exc:
        _log.exception(
            "Unhandled error during command '%s': %s",
            args.command,
            exc
        )
        sys.exit(1)
    finally:
        engine.dispose()
        _log.info("Engine disposed.")

if __name__ == "__main__":
    main()
