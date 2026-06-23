from __future__ import annotations
from typing import Literal
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator, Field

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.

    This class uses Pydantic's `BaseSettings` to automatically read values
    from environment variables and a `.env` file. It provides typed access to
    critical runtime configuration, including the database connection URL,
    the default schema, and the deployment environment.

    Attributes:
        DB_SCHEMA (str): The default database schema name used for all
            application tables, functions, and triggers. Defaults to
            `"geopolitical_tracker"`. This value is used in Alembic migrations
            and at runtime to set the PostgreSQL `search_path`.
        DB_URL (PostgresDsn): A PostgreSQL connection URL (DSN) that includes
            the host, port, database name, and credentials. This is a required
            field and must be set either via the environment variable
            `DB_URL` or in the `.env` file. It is validated by the
            `check_db_url` validator.
        ENV (Literal["production", "development"]): The runtime environment.
            Defaults to `"development"`. This can be used to enable
            environment‑specific behavior (e.g., debug logging, mock data).
            The environment variable `ENV` overrides this default.

    Environment variable mapping:
        - `DB_URL` → `DB_URL` (required)
        - `DB_SCHEMA` → `DB_SCHEMA` (optional, defaults as above)
        - `ENV` → `ENV` (optional, defaults to `"development"`)

    The `.env` file must be placed in the same directory as this module
    (i.e., `src/config/`). The file is encoded in UTF‑8.

    Configuration behavior:
        - `case_sensitive=True`: Environment variable names must match the
          attribute names exactly (case‑sensitive).
        - `extra='ignore'`: Any extra environment variables not defined in
          this class are silently ignored, preventing accidental overrides.

    Raises:
        ValueError: During instantiation if `DB_URL` is not set (or is `None`),
            as enforced by the `check_db_url` validator.

    Example:
        ```python
        from src.config.config import get_settings
        settings = get_settings()
        print(settings.DB_URL)  # postgresql://user:pass@localhost:5432/db
    """
    DB_SCHEMA: str = Field(
        default=...,
        description="Database schema name"
    )
    DB_URL: PostgresDsn = Field(
        default=...,
        description="PostgreSQL connection URL"
    )
    ENV: Literal["production", "development"] = Field(
        default=...,
        description="Runtime environment"
    )
    
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / '.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )
    
    @field_validator("DB_URL", mode="before")
    @classmethod
    def check_db_url(cls, v: PostgresDsn) -> PostgresDsn:
        """
        Validate that the `DB_URL` configuration value is provided and non‑empty.

        This validator runs **before** Pydantic attempts to parse the value into
        a `PostgresDsn` type (because `mode="before"`). It checks if the incoming
        value is `None`. If so, it raises a `ValueError` with a clear error message
        instructing the user to set the environment variable or create a `.env` file.

        This validation is critical because the database URL is required for the
        application to function. Without it, the application cannot connect to the
        database, and migrations cannot run.

        Parameters:
            v (PostgresDsn): The raw input value from the environment (before
                parsing). Typically a string or `None`.

        Returns:
            PostgresDsn: The validated value (unchanged) if it is not `None`.

        Raises:
            ValueError: If `v` is `None`, indicating that the `DB_URL` environment
                variable is missing.

        Notes:
            - This validator is applied only to the `DB_URL` field.
            - The error message provides guidance for both production and
            development setups, suggesting the creation of a `.env` file.
            - The `@classmethod` decorator is required for Pydantic v2 validators.
        """
        if v is None:
            raise ValueError(
                "DB_URL environment variable is not set. "
                "In production this is fatal. For local development, "
                "create a .env file and define DB_URL=. "
                "Then set ENV=development if needed."
            )
        return v

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()