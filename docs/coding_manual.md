# Comprehensive Incident Coding Manual

## Introduction

This manual consolidates all taxonomic frameworks, operational definitions, coding protocols, and decision trees for consistent incident coding. Use it as the authoritative reference during data population.

---

## Taxonomic Frameworks and Coding Protocols

### Two-Tier Event Taxonomy with Operational Definitions

#### Diplomatic Event Category

**Code**: `DIPLMTC`
**Name**: Diplomatic Event Category
**Definition**: Diplomatic events encompass government-to-government engagement, communication, and institutional interaction involving official representatives of nation-states or multilateral organizations. The diplomatic category focuses on political-relationship dimensions rather than military-operational or economic-transactional aspects, though significant overlap exists requiring hierarchical precedence rules specified below.

**Subcategories**: 
**Code**: `HI_LVL_SMIT`
**Name**: High-Level Summit
**Definition**: Meetings involving heads of state (presidents, monarchs), heads of government (prime ministers, chancellors), or equivalent executive leaders at bilateral or multilateral forums. Includes formal state visits, bilateral summit meetings, and participation in institutionalized multilateral summit frameworks (ASEAN Summit, ASEAN+3, East Asia Summit, ASEAN Regional Forum at leaders' level).

**Inlcusion Criteria**: 
- Meeting participants include at least one head of state/government.
- Formal agenda with documented outcomes (joint statements, communiqués, memoranda of understanding).
- Official government announcement or media coverage confirming summit occurrence.
- Substantive policy discussions beyond purely ceremonial functions.

**Exclusion Criteria**: 
- Ministerial-level meetings without executive leadership participation (code as Ministerial Engagement).
- Informal encounters at multilateral gatherings without substantive bilateral engagement (brief hallway conversations during UN General Assembly not coded unless generating specific outcomes).
- Purely ceremonial events without policy substance (ribbon-cutting ceremonies, cultural performances attended by leaders).

**Boundary Cases**: 
- Virtual Summits: Include video-conference summit meetings if they possess formal agendas and documented outcomes comparable to in-person summits.
- Summit Cancellations: Code announced summits that are subsequently cancelled or postponed as Diplomatic Signaling if the cancellation itself carries strategic messaging significance (e.g., Philippine President Duterte cancelling planned visit to Japan in 2016 following international criticism).
- Side Meetings at multilateral forums: Code substantive bilateral meetings occurring on margins of larger multilateral gatherings (e.g., Xi-Biden bilateral meeting at G20 Summit) if they generate distinct outcomes, separate from the parent multilateral event.

**Anchoring Examples**: 
| Event | Date | Location | Description | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **ASEAN Summit** | November 2022 | Phnom Penh, Cambodia | Annual ASEAN Summit attended by all ten heads of government, discussing South China Sea Code of Conduct negotiations, Myanmar crisis, and economic integration initiatives | High, documented through ASEAN Chairman's Statement and bilateral meeting readouts |
| **U.S.-ASEAN Special Summit** | May 2022 | Washington, D.C., United States | President Biden hosts all ten ASEAN leaders for unprecedented Washington summit, elevating U.S.-ASEAN relations to Comprehensive Strategic Partnership | Critical, marking shift in U.S. regional engagement strategy |
| **Xi Jinping State Visit to Philippines** | November 2018 | Maynila (Manila), Philippines | Chinese President Xi Jinping conducts state visit to Manila, meeting President Duterte, signing 29 bilateral agreements covering infrastructure, trade, and defense cooperation | High, symbolizing Philippines' strategic pivot toward China during Duterte administration |
| **Singapore-Indonesia Leaders' Retreat** | January 2022 | Pulau Bintan (Bintan), Indonesia | Prime Minister Lee Hsien Loong and President Joko Widodo hold annual retreat discussing bilateral cooperation, regional economic recovery, and ASEAN leadership | Medium, routine institutionalized bilateral mechanism |
| **East Asia Summit** | November 2023 | DKI Jakarta (Jakarta), Indonesia | Leaders from 18 countries (10 ASEAN + 8 dialogue partners) convene for annual forum addressing maritime security, economic resilience, climate change, with particular focus on South China Sea tensions and Myanmar crisis | High, primary leaders-level platform for Asia-Pacific security dialogue |

**Code**: `MINSTRL_ENGMT`
**Name**: Ministerial Engagement
**Definition**: Meetings, joint statements, or coordinated activities involving cabinet-level government officials below head of state/government rank, including foreign ministers, defense ministers, trade/commerce ministers, and other senior appointed officials. Encompasses bilateral ministerial dialogues, multilateral ministerial meetings within ASEAN frameworks, and "2+2" format dialogues combining foreign and defense ministers.

**Inclusion Criteria**: 
- Participants hold ministerial or equivalent senior appointed government positions.
- Formal meeting agenda with policy substance.
- Official documentation through joint statements, memoranda, or government press releases.
- Represents official government policy positions.

**Exclusion Criteria**: 
- Working-level official meetings (deputy minister, director-general levels typically excluded unless extraordinary circumstances).
- Private sector or non-governmental delegations even if involving former officials.
- Academic or track-two dialogues lacking official government representation.

**Boundary Cases**: 
- Special envoys and presidential representatives: Include if they carry explicit authority to represent head of state/government in negotiations (e.g., U.S. Presidential Special Envoy for Climate meeting ASEAN counterparts).
- Defense minister + military chief combinations: Code as Ministerial Engagement based on presence of cabinet-level minister, even if accompanied by uniformed military leadership.
- Ministerial participation at multilateral conferences: Code only substantive bilateral ministerial meetings or significant multilateral ministerial outcomes, not mere attendance at conferences.

**Anchoring Examples**: 
| Event | Date | Location | Description | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **ASEAN Foreign Ministers' Meeting** | February 2021 | Virtual | All ten ASEAN foreign ministers convene emergency meeting on Myanmar coup, issuing consensus statement calling for dialogue and peaceful resolution | High, ASEAN's primary response mechanism to Myanmar crisis |
| **U.S.-Philippines 2+2 Ministerial Dialogue** | July 2022 | Maynila (Manila), Philippines | U.S. Secretaries of State and Defense meet Philippine counterparts, announcing expansion of Enhanced Defense Cooperation Agreement sites and reaffirming mutual defense treaty commitments | High, substantive defense cooperation enhancement |
| **China-ASEAN Foreign Ministers' Special Meeting** | June 2020 | Virtual | Chinese Foreign Minister Wang Yi hosts special virtual meeting with ASEAN counterparts on COVID-19 cooperation and South China Sea Code of Conduct negotiation | Medium, routine diplomatic engagement with some substantive outcomes |
| **ASEAN Defense Ministers' Meeting Plus (ADMM-Plus)** | June 2023 | Singapore, Singapore | Defense ministers from ASEAN and eight dialogue partners convene for biennial meeting addressing maritime security, humanitarian assistance, cyber defense, and counterterrorism cooperation | Medium, institutionalized multilateral defense dialogue mechanism |
| **India-Viet Nam Defense Minister Meeting** | June 2022 | New Delhi, India | Indian and Vietnamese defense ministers meet to discuss defense industry cooperation, naval collaboration, and capacity building, signing implementation protocol for existing defense agreement | Medium, bilateral defense relationship strengthening |

**Code**: `DIPLMTC_SIGNLN`
**Name**: Diplomatic Signaling
**Definition**: Official government communications, statements, protests, or symbolic actions intended to convey policy positions, register objections, signal commitment, or influence other actors' behavior through public or private diplomatic channels. Includes diplomatic notes/démarches, official protests, public statements by spokespersons or leaders, ambassador recalls or expulsions, and symbolic diplomatic gestures.

**Inclusion Criteria**: 
- Communication originates from official government channels (foreign ministry spokespersons, official government statements, diplomatic correspondence).
- Content addresses specific policy issues, incidents, or interstate relations.
- Clear signaling intent regarding positions, objections, or commitments.
- Documented through government websites, press releases, or credible media reporting of official statements.

**Exclusion Criteria**: 
- Unofficial statements by individual politicians not representing formal government positions.
- Academic or think tank analyses even if authored by former officials.
- Media speculation about government positions without official confirmation.
- Social media posts by officials unless representing formal government communications.

**Boundary Cases**: 
- Head of state/government public speeches: Code substantive policy announcements or position statements as Diplomatic Signaling; ceremonial remarks without policy content excluded.
- Diplomatic notes without public disclosure: Include if existence and general content confirmed through credible sources, even if full text not publicly available.
- Implicit signaling through action: Code symbolic actions with clear diplomatic messaging intent (e.g., military parade on disputed territory anniversary, choosing summit participation timing to signal displeasure).

**Anchoring Examples**: 
| Event | Date | Location | Description | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Philippine Diplomatic Protest to China** | November 2021 | Maynila (Manila), Philippines | Philippines Department of Foreign Affairs issues formal protest note to China regarding "swarming and threatening presence" of Chinese maritime militia vessels near Pag-asa Island (Thitu Island) in Spratlys | Medium, routine but documented assertion of sovereignty claims |
| **ASEAN Foreign Ministers' Statement on South China Sea** | August 2020 | Virtual | ASEAN foreign ministers issue rare joint statement expressing concern over "serious incidents in the South China Sea" and reaffirming commitment to international law including UNCLOS | High, unusual ASEAN consensus statement addressing contentious issue |
| **Myanmar Recalls Ambassador from Singapore** | March 2021 | Nay Pyi Taw (Naypyidaw), Myanmar | Singapore announces recall of its ambassador to Myanmar and downgrading of diplomatic representation following February coup, one of strongest ASEAN diplomatic responses | High, rare ASEAN member public censure of fellow member |
| **U.S. Statement Rejecting China's South China Sea Claims** | July 2020 | Washington, D.C., United States | U.S. Secretary of State issues statement declaring China's South China Sea maritime claims "completely unlawful," explicitly rejecting Chinese positions and aligning with 2016 arbitral tribunal ruling | Critical, shift in U.S. declaratory policy from neutrality to explicit position-taking |
| **Viet Nam Protest Over Chinese Survey Ship** | July 2019 | Vanguard Bank | Viet Nam's Foreign Ministry issues protest note and public statement condemning Chinese survey vessel operations near Vanguard Bank within Viet Nam's exclusive economic zone | Medium, recurring pattern of Vietnamese diplomatic objections to Chinese activities |

**Code**: `INSTNL_MECH`
**Name**: Institutional Mechanism
**Definition**: Establishment, modification, significant activities, or termination of formal diplomatic institutions, multilateral frameworks, bilateral mechanisms, treaties, or organizational structures governing interstate relations. Includes creation of new dialogue platforms, treaty ratifications, institutionalized mechanism launches, and significant organizational reforms.

**Inclusion Criteria**: 
- Formal establishment or modification of institutional structures.
- Treaty signing, ratification, or entry into force.
- Launch of new dialogue mechanisms or frameworks.
- Significant procedural or structural changes to existing institutions.
- Official documentation through treaties, memoranda of understanding, joint declarations.

**Exclusion Criteria**: 
- Routine meetings of existing mechanisms without structural changes (code under appropriate meeting type - Summit, Ministerial Engagement).
- Informal dialogue proposals not resulting in institutional establishment.
- Expired or inactive mechanisms without documented termination or significant renewal.

**Boundary Cases**: 
- Mechanism upgrades: Code elevation of relationship status (e.g., Strategic Partnership to Comprehensive Strategic Partnership) as Institutional Mechanism if accompanied by formal framework documents or structural changes.
- Treaty renewals: Code automatic renewals of existing treaties only if renewal involves renegotiation, amendment, or significant policy debate; routine administrative renewals excluded.
- Non-binding frameworks: Include "outlooks," "visions," or "frameworks" even if not legally binding treaties, if they establish new institutional structures or mechanisms.

**Anchoring Examples**: 
| Event | Date | Location | Description | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **ASEAN Outlook on Indo-Pacific Adoption** | June 2019 | Krung Thep Maha Nakhon (Bangkok), Thailand | ASEAN adopts official "ASEAN Outlook on the Indo-Pacific" document establishing ASEAN's framework for engagement with Indo-Pacific strategic concept, asserting ASEAN centrality | High, ASEAN's strategic response to great power Indo-Pacific competition |
| **Regional Comprehensive Economic Partnership (RCEP) Entry into Force** | January 2022 | — | World's largest free trade agreement enters force after ratification by required threshold of signatories (10 ASEAN states plus China, Japan, South Korea, Australia, New Zealand), creating integrated economic bloc | Critical, major economic integration milestone |
| **AUKUS Partnership Announcement** | September 2021 | Virtual | Australia, United Kingdom, United States announce trilateral security partnership (AUKUS) including nuclear-powered submarine technology transfer, reshaping Indo-Pacific security architecture | Critical, major strategic realignment with implications for regional balance |
| **Enhanced Defense Cooperation Agreement (EDCA)** | April 2014 | Maynila (Manila), Philippines | Bilateral defense agreement allowing rotational U.S. military presence at Philippine bases enters force; expanded in 2023 to include four additional sites (with 2023 expansion) | High, institutional foundation for U.S.-Philippine defense cooperation enhancement |
| **ASEAN-China Code of Conduct Negotiations Launch** | — | Maynila (Manila), Philippines | ASEAN and China formally launch negotiations for binding Code of Conduct in South China Sea, establishing institutional negotiation framework (ongoing, substantive agreement remains unachieved as of 2024) | High, institutional mechanism attempting to manage maritime disputes |

#### Economic Event Category

**Code**: `ECON`
**Name**: Economic Event Category
**Definition**: Economic events encompass trade, investment, financing, and economic policy interactions between states or involving state economic measures affecting regional dynamics. The category includes both cooperative economic integration mechanisms and coercive economic statecraft, distinguished by intent and context. Economic events possess clear commercial or financial dimensions beyond purely political or military aspects.

**Subcategories**: 
**Code**: `TRADE_AGMNT`
**Name**: Trade Agreement
**Definition**: Bilateral or multilateral agreements governing trade relations including free trade agreements, preferential trade arrangements, tariff modifications, customs procedures, and trade facilitation frameworks. Encompasses agreement negotiations, signings, ratifications, entries into force, and significant implementation milestones or disputes.

**Inclusion Criteria**: 
- Formal government-to-government agreements with documented texts.
- Substantive trade provisions affecting tariffs, market access, or regulatory harmonization.
- Official negotiation rounds with documented progress or outcomes.
- Agreement implementation milestones or dispute resolution proceedings.

**Exclusion Criteria**: 
- Private commercial contracts between companies without government involvement.
- Investment agreements lacking trade dimensions (code as Investment and Financing).
- General economic cooperation statements without binding trade commitments.

**Boundary Cases**: 
- Comprehensive economic agreements: Code agreements combining trade, investment, and services provisions as Trade Agreement if trade liberalization constitutes primary component; as Investment and Financing if infrastructure or capital flows dominate.
- Trade disputes: Code formal dispute resolution proceedings under trade agreements (WTO complaints, FTA arbitration) as Trade Agreement events documenting institutional operation.
- Negotiation failures: Code collapse of trade negotiations as Trade Agreement events if failure itself carries strategic significance (e.g., U.S. withdrawal from Trans-Pacific Partnership negotiations).

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Regional Comprehensive Economic Partnership (RCEP) Signing** | November 2020 | Virtual | Fifteen Asia-Pacific nations (10 ASEAN + China, Japan, South Korea, Australia, New Zealand) sign world's largest trade agreement after eight years of negotiations, creating integrated market of 2.2 billion people | Critical, major economic integration milestone excluding United States |
| **Indonesia-Australia Comprehensive Economic Partnership Agreement Entry into Force** | July 2020 | — | Bilateral FTA enters force after ratification, eliminating tariffs on 94% of Indonesian exports and 99% of Australian exports, including sensitive agricultural sectors | Medium, bilateral economic relationship deepening |
| **U.S.-China Phase One Trade Deal** | January 2020 | Washington, D.C., United States | United States and China sign partial trade agreement pausing tariff escalation and committing China to increased U.S. agricultural purchases, affecting ASEAN supply chain calculations | High, temporary de-escalation of U.S.-China trade war with regional spillover implications |
| **ASEAN Trade in Goods Agreement (ATIGA) Amendments** | September 2021 | Virtual | ASEAN members approve amendments to intra-ASEAN trade agreement enhancing rules of origin flexibility and customs procedures harmonization, advancing economic integration | Medium, incremental improvement to existing frameworks |
| **Viet Nam-EU Free Trade Agreement (EVFTA) Implementation** | August 2020 | — | Comprehensive FTA between Viet Nam and European Union enters force, eliminating 99% of tariffs and providing Viet Nam preferential access to European markets | High, Viet Nam's economic diversification strategy beyond China dependence |

**Code**: `INVST_FIN`
**Name**: Investment and Financing
**Definition**: Infrastructure financing initiatives, bilateral investment treaties, development bank lending, major capital project agreements, foreign direct investment policy changes, and public financing arrangements. Encompasses both multilateral development financing and bilateral government-backed investment projects, particularly Belt and Road Initiative projects and alternative connectivity initiatives.

**Inclusion Criteria**: 
- Government-to-government financing agreements or sovereign guarantees.
- Multilateral development bank lending with strategic policy dimensions.
- Major infrastructure projects with state-owned enterprise or government backing.
- Bilateral investment treaty negotiations, signings, or dispute settlements.
- Foreign investment policy changes affecting regional capital flows.

**Exclusion Criteria**: 
- Purely private commercial investments without government involvement or strategic implications.
- Routine development bank project lending without significant policy dimensions.
- Corporate mergers and acquisitions unless involving state-owned enterprises or triggering investment screening.

**Boundary Cases**: 
- BRI projects: Code Belt and Road Initiative projects as Investment and Financing regardless of implementing entity if projects receive Chinese government backing or strategic emphasis in bilateral relations.
- Investment screening: Code establishment or application of foreign investment security review mechanisms (CFIUS-type systems) as Investment and Financing when targeting specific countries or sectors with strategic implications.
- Debt sustainability crises: Code debt renegotiations or restructurings of strategic infrastructure projects as Investment and Financing events documenting economic statecraft consequences.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **China-Indonesia High-Speed Rail Project Completion** | October 2023 | DKI Jakarta (Jakarta)-Kota Bandung (Bandung), Indonesia | First phase of Chinese-financed Jakarta-Bandung high-speed rail opens, Belt and Road Initiative flagship project after numerous delays and cost overruns | High, demonstration of BRI infrastructure delivery capacity and challenges |
| **Japan-ASEAN Connectivity Initiative Funding Announcement** | November 2019 | Krung Thep (Bangkok), Prathet Thai (Thailand) | Japan announces $billions in infrastructure financing for Southeast Asian connectivity projects, positioned as alternative to Belt and Road Initiative emphasizing quality infrastructure and debt sustainability | High, competitive infrastructure financing by external powers |
| **U.S. International Development Finance Corporation (DFC) Southeast Asia Investment** | June 2021 | — | DFC approves financing for multiple Southeast Asian infrastructure and technology projects as part of Build Back Better World initiative countering BRI | Medium, U.S. attempt to provide BRI alternative through development finance |
| **Sri Lanka Hambantota Port Debt-for-Equity Swap** | July 2017 | Ambaanthottai (Hambantota), Ilankai (Sri Lanka) | Sri Lanka transfers Chinese-financed port to 99-year Chinese lease due to debt servicing inability, generating regional concerns about debt-trap diplomacy affecting ASEAN BRI calculations (regional spillover implications) | High, cautionary precedent influencing regional BRI reception |
| **Asian Infrastructure Investment Bank (AIIB) Lending to ASEAN Projects** | — | — | China-initiated multilateral development bank approves multiple Southeast Asian infrastructure financing projects, establishing institutional alternative to Western-dominated World Bank/ADB (ongoing) | Medium per project, cumulative High for regional financing architecture |
      
**Code**: `ECON_CORCN`
**Name**: Economic Coercion
**Definition**: Economic measures employed coercively to influence political behavior or punish policy positions, including sanctions, export controls, import restrictions, market access denial, investment screening targeting specific countries, and other economic tools used with explicit or implicit political conditionality. Distinguishes from routine trade policy through coercive intent linked to political objectives.

**Inclusion Criteria**: 
- Economic measures explicitly linked to political grievances or demands in official statements or credible analysis.
- Informal or unofficial economic restrictions targeting specific countries (customs delays, regulatory harassment, unofficial bans).
- Sanctions regimes imposed for political rather than commercial reasons.
- Export controls or investment restrictions targeting specific countries for strategic competition.
- Clear temporal correlation between political disputes and economic measures.

**Exclusion Criteria**: 
- Routine trade remedies (antidumping, countervailing duties) based on economic criteria without political linkages.
- Multilateral sanctions with broad international support and clear legal violations (UN Security Council sanctions).
- Economic measures with purely commercial justification (food safety standards, technical regulations) absent political context.

**Boundary Cases**: 
- Informal restrictions: Code unofficial bans, customs delays, or regulatory obstacles as Economic Coercion if multiple credible sources identify political motivations and targeted country patterns.
- Ambiguous causation: When economic measures occur contemporaneously with political disputes but official justifications cite commercial reasons, code as Economic Coercion if circumstantial evidence (timing, selective targeting, reversal following political accommodation) suggests political motivations.
- Withdrawal of economic benefits: Code removal of preferential treatment or cancellation of announced investments/projects as Economic Coercion if occurring in political dispute contexts.

**Anchoring Examples**: 
| Event | Date | Location | Definition / Description | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **China Informal Banana Import Restrictions on Philippines** | July 2016 | China (ports) | Following Permanent Court of Arbitration ruling favoring Philippines in South China Sea dispute, Chinese customs imposes heightened inspection requirements causing Philippine banana exports to rot at ports, interpreted as economic retaliation | High, gray-zone economic coercion without formal sanctions |
| **U.S. Semiconductor Export Controls Affecting China-ASEAN Supply Chains** | October 2022 | Washington, D.C., United States | United States implements sweeping export controls restricting advanced semiconductor equipment and technology transfers to China, affecting regional electronics manufacturing supply chains and forcing ASEAN firms to navigate technology decoupling. | Critical, economic dimension of U.S.-China strategic competition restructuring regional production networks |
| **China Rare Earth Export Restrictions** | December 2010 | Beijing, China | China restricts rare earth element exports during territorial disputes with Japan, demonstrating economic leverage and influencing subsequent ASEAN strategic calculations regarding resource dependencies (precedent relevant to ASEAN context) | High as precedent informing regional supply chain diversification strategies |
| **U.S. Sanctions on Myanmar Military Leaders Following 2021 Coup** | February 2021 | Washington, D.C., United States | U.S. Treasury targets Myanmar military leaders following February 2021 coup and violence against protesters | High, economic response to political crisis generating regional spillover effects |
| **EU Sanctions on Myanmar State-Owned Enterprises Following 2021 Coup** | March 2021 | Brussels, Belgium | EU imposes asset freezes and travel bans on entities linked to Myanmar military following February 2021 coup and violence against protesters | High, economic response to political crisis generating regional spillover effects |
| **UK Sanctions on Myanmar Military Conglomerates Following 2021 Coup** | April 2021 | London, United Kingdom | UK sanctions Myanmar military-owned businesses operating in multiple sectors following February 2021 coup and violence against protesters | High, economic response to political crisis generating regional spillover effects |
| **Australia-China Economic Tensions** | May 2020 | Beijing, China | China imposes trade restrictions on multiple Australian commodity exports (barley, wine, coal, timber) following Australian calls for COVID-19 origin investigation, creating opportunities for ASEAN commodity exporters to fill market gaps (affecting ASEAN trade flows) | High, demonstrating economic coercion patterns and regional trade diversion effects |

**Code**: `SUPLY_CHAIN_INIT`
**Name**: Supply Chain Initiative
**Definition**: Government-led initiatives addressing supply chain resilience, diversification, critical mineral access, technology transfer arrangements, and production network reconfiguration. Encompasses policies responding to pandemic disruptions, U.S.-China decoupling pressures, and efforts to reduce strategic dependencies through friend-shoring, near-shoring, or domestic capacity building.

**Inclusion Criteria**: 
- Government policies or agreements explicitly addressing supply chain issues.
- Critical mineral or rare earth element cooperation agreements.
- Technology transfer or domestic manufacturing capacity building with supply chain rationale.
- Multilateral frameworks addressing supply chain resilience (Indo-Pacific Economic Framework supply chain pillar).
- Corporate relocation or investment incentives with strategic supply chain diversification objectives.

**Exclusion Criteria**: 
- Routine foreign direct investment without supply chain diversification strategic framing.
- General industrial policy without explicit supply chain risk mitigation objectives.
- Private corporate supply chain decisions without government policy linkages.

**Boundary Cases**: 
- COVID-19 pandemic responses: Code supply chain policies emerging from pandemic disruptions as Supply Chain Initiative if they establish enduring structural changes beyond immediate crisis response.
- Technology decoupling: Code policies promoting domestic semiconductor, telecommunications, or advanced technology production capacity as Supply Chain Initiative when motivated by reducing dependencies or technology competition.
- Regional production networks: Code ASEAN initiatives promoting intra-regional supply chain integration (ASEAN automotive components cooperation, ASEAN electronics production networks) as Supply Chain Initiative if driven by resilience or strategic objectives.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Indo-Pacific Economic Framework (IPEF) Supply Chain Agreement** | November 2023 | San Francisco, United States | Fourteen Indo-Pacific nations including seven ASEAN members agree to supply chain cooperation framework establishing crisis response mechanisms, diversification initiatives, and transparency commitments | High, U.S.-led economic architecture initiative in Indo-Pacific lacking tariff liberalization |
| **U.S.-Viet Nam Semiconductor Cooperation** | September 2023 | Ha Noi (Hanoi), Viet Nam | United States and Viet Nam announce initiatives promoting Vietnamese semiconductor manufacturing capacity as part of supply chain diversification from China, including technology partnerships and investment incentives | High, U.S. efforts to build alternative semiconductor supply chains |
| **China-ASEAN Rare Earth Industrial Cooperation** | December 2021 | Ganzhou, China | China announces expanded rare earth processing cooperation with ASEAN countries, maintaining regional supply chain dominance while potentially creating dependencies | Medium, Chinese efforts to preserve critical mineral supply chain centrality |
| **ASEAN Automotive Integration Initiatives** | November 2004 | Viang Chan (Vientiane), Lao PDR (Laos) | ASEAN members implement policies promoting regional automotive component supply chain integration reducing extra-regional dependencies and enhancing collective competitiveness. Foundational agreement included to illustrate long-term policy evolution | Medium, intra-ASEAN economic integration with supply chain resilience dimensions |
| **Japan-ASEAN Supply Chain Resilience Initiative** | April 2020 | Virtual | Japanese government launches program subsidizing Japanese companies to diversify production from China to Southeast Asia, accelerating post-pandemic supply chain reconfiguration | High, government-led production network restructuring affecting regional investment flows |

#### Military Event Category

**Code**: `MLITR`
**Name**: Military Event Category
**Definition**: Military events encompass activities by state armed forces, paramilitary entities, and defense-related operations including exercises, deployments, operational activities, defense cooperation, and armed incidents. The category focuses on security and defense dimensions of state behavior, distinguishing from diplomatic engagement (though defense summits may be coded as Ministerial Engagement if diplomatic dimensions predominate) and economic arrangements (though arms sales and defense industry cooperation may overlap with Investment and Financing requiring hierarchical coding rules).

**Subcategories**: 
**Code**: `MRITM_OPS`
**Name**: Maritime Operations
**Definition**: Naval vessel, coast guard, or maritime militia activities in regional waters including freedom of navigation operations, maritime patrols, vessel encounters, blockade or interception operations, and activities in contested or disputed maritime zones. Encompasses both routine operational activity with strategic signaling dimensions and confrontational encounters.

**Inclusion Criteria**: 
- State naval, coast guard, or paramilitary maritime forces operations.
- Operations in disputed waters or near contested features.
- Freedom of navigation operations explicitly asserting maritime rights.
- Vessel encounters involving shadowing, blocking, or confrontational behavior.
- Maritime surveillance or intelligence collection operations with strategic dimensions.

**Exclusion Criteria**: 
- Routine maritime patrols without strategic signaling or dispute dimensions.
- Commercial shipping incidents lacking state military/paramilitary involvement.
- Piracy incidents unless involving state responses or non-state armed groups with political dimensions.

**Boundary Cases**: 
- Coast guard vs. navy operations: Code all state maritime operations as Maritime Operations regardless of whether navy or coast guard executes, as distinction often reflects bureaucratic organization rather than operational substance.
- Maritime militia: Code Chinese People's Armed Forces Maritime Militia operations as Maritime Operations despite civilian vessel appearance, given state coordination and strategic employment.
- Multi-domain incidents: Code incidents involving both maritime and air dimensions (naval vessels + military aircraft) as Maritime Operations if maritime component predominates; as Airspace Operations if air component drives the incident.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **U.S. Freedom of Navigation Operation (FONOP)** | January 2023 | Mischief Reef | U.S. Navy destroyer conducts transit within 12 nautical miles of Chinese-occupied Mischief Reef in Spratlys, explicitly challenging Chinese excessive maritime claims and asserting international law rights | High, routine but symbolically important assertion of legal positions |
| **China Coast Guard Blocking Philippine Resupply Mission** | August 2023 | Second Thomas Shoal | Chinese Coast Guard vessels employ water cannons against Philippine Coast Guard and supply boats attempting to resupply troops stationed aboard grounded BRP Sierra Madre, escalating gray-zone coercion tactics | High, intensification of coercive methods short of armed force |
| **Chinese Maritime Militia Swarming** | March 2021 | Whitsun Reef | Over 200 Chinese fishing vessels identified as maritime militia elements anchor at Whitsun Reef (Julian Felipe Reef) in Philippine EEZ, remaining despite Philippine diplomatic protests, asserting presence in disputed waters | High, large-scale gray-zone operation generating regional concerns |
| **Indonesia-China Coast Guard Standoff** | January 2020 | Kepulauan Natuna (Natuna Islands), Indonesia EEZ | Chinese Coast Guard vessels escort Chinese fishing boats operating in Indonesian EEZ near Natuna Islands, prompting Indonesian naval and air deployments and diplomatic protests, testing Indonesian sovereignty claims | High, Chinese probing of Indonesian resolve in overlapping claim areas |
| **Vietnamese-Chinese Naval Confrontation** | July 2019 | Vanguard Bank | Chinese survey vessel Haiyang Dizhi 8 and coast guard escorts operate within Vietnamese-claimed continental shelf near Vanguard Bank for months, shadowed by Vietnamese naval and coast guard vessels in tense standoff | High, prolonged confrontation over resource exploration rights |

**Code**: `MLITR_EXS`
**Name**: Military Exercises
**Definition**: Bilateral or multilateral military training exercises including live-fire drills, field training exercises, naval exercises, air exercises, combined arms exercises, command post exercises, tabletop simulations, and humanitarian assistance/disaster relief (HADR) exercises. Encompasses exercise planning announcements, execution, and post-exercise assessments with strategic signaling dimensions.

**Inclusion Criteria**: 
- Formal military exercises with multiple participating units or countries.
- Official announcements or military press releases documenting exercises.
- Exercises with strategic signaling dimensions (location, timing, participants, scenarios).
- HADR exercises with military participation even if focused on non-combat operations.

**Exclusion Criteria**: 
- Internal unit-level training without bilateral/multilateral dimensions or strategic signaling.
- Routine readiness training unless occurring in strategically significant contexts (e.g., training near disputed territories).
- Civilian disaster preparedness exercises without military participation.

**Boundary Cases**: 
- Exercise scale thresholds: Code exercises regardless of scale if they involve bilateral/multilateral participation or occur in strategically significant contexts; exclude purely internal platoon/company-level training.
- HADR vs. combat exercises: Code both HADR and combat exercises as Military Exercises, potentially noting exercise focus in descriptions for analytical differentiation.
- Sequential exercises: Code each discrete exercise as separate event even if occurring in rapid succession as part of broader military engagement campaigns.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Balikatan U.S.-Philippines Exercise** | April 2023 | Pilipinas (Philippines) | Annual bilateral exercise involving 17,600 troops, largest iteration in decades, including coastal defense scenarios and expanded to four additional sites under EDCA, signaling alliance strengthening amid South China Sea tensions | High, demonstration of treaty alliance operational cooperation |
| **China-Russia Joint Sea Naval Exercise** | October 2021 | Zaliv Petra Velikogo (Peter the Great Gulf), Sea of Japan, Rossiya (Russia) | Chinese and Russian navies conduct joint exercise in Sea of Japan and Western Pacific including anti-submarine warfare and air defense drills, demonstrating strategic coordination amid both countries' tensions with United States | High, China-Russia military cooperation intensification |
| **Super Garuda Shield Multilateral Exercise** | August 2022 | Baturaja, Sumatera Selatan (South Sumatra), Indonesia | Expanded exercise involving 14 nations including ASEAN members (Indonesia, Singapore), United States, Australia, Japan, conducting amphibious operations and jungle warfare training in Indonesian territory | Medium-high, multilateral military cooperation framework expansion |
| **ASEAN Defense Ministers' Meeting Plus (ADMM-Plus) Field Training Exercise** | October 2023 | Ngayogyakarta (Yogyakarta), Indonesia | Multilateral HADR exercise involving military forces from ASEAN and dialogue partner nations practicing disaster response coordination, institutional mechanism operationalization | Medium, ASEAN-led multilateral security cooperation practical implementation |
| **India-Viet Nam PASSEX Naval Exercise** | December 2020 | South China Sea | Indian Navy and Viet Nam People's Navy conducted a two-day Passage Exercise (PASSEX) in the South China Sea following India's delivery of humanitarian relief supplies to flood-affected regions of central Viet Nam. The exercise aimed to reinforce maritime interoperability and jointness between the two navies | Medium, represented growing India-Viet Nam defence cooperation against China's assertiveness in the South China Sea |

**Code**: `DFNC_COOP`
**Name**: Defense Cooperation
**Definition**: Defense agreements, mutual defense treaties, access arrangements enabling foreign military presence, intelligence sharing arrangements, defense industry partnerships, military aid programs, and security assistance. Encompasses agreement negotiations, signings, renewals, implementation milestones, and significant capability transfers (though large-scale arms sales with strategic implications may overlap with Investment and Financing).

**Inclusion Criteria**: 
- Formal defense agreements or treaties with documented texts or official announcements.
- Base access agreements or status of forces agreements (SOFAs).
- Defense industry cooperation including technology transfer or joint production.
- Military aid or security assistance programs with strategic dimensions.
- Intelligence sharing arrangements if publicly acknowledged.

**Exclusion Criteria**: 
- Commercial arms sales without government-to-government dimensions (though most significant arms transfers involve state-to-state agreements).
- Defense diplomatic exchanges without substantive cooperation commitments.
- Routine implementation of existing agreements without significant new developments.

**Boundary Cases**: 
- Arms sales: Code major arms sales (combat aircraft, naval vessels, advanced systems) as Defense Cooperation if they involve government-to-government agreements and strategic implications; code as Investment and Financing if commercial/economic dimensions predominate.
- Training programs: Code establishment of formal military training programs or education exchanges as Defense Cooperation if they represent institutional relationship elements; exclude individual personnel exchanges unless part of broader strategic initiatives.
- Access vs. basing: Code both rotational access arrangements and permanent basing agreements as Defense Cooperation, noting distinction in descriptions for analytical purposes.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Enhanced Defense Cooperation Agreement (EDCA) Expansion** | April 2023 | Maynila (Manila), Pilipinas (Philippines) | Philippines grants United States access to four additional military bases (total nine sites) under EDCA framework, including locations in northern Luzon facing Taiwan and Palawan facing South China Sea, significantly expanding U.S. regional military posture | Critical, major alliance infrastructure enhancement amid China tensions |
| **Australia-Singapore Comprehensive Strategic Partnership including Defense Cooperation** | — | Singapore, Singapore | Comprehensive bilateral framework including Australian military training access to Singapore facilities, joint exercises, defense industry cooperation, and intelligence sharing (ongoing) | High, institutionalized bilateral defense partnership |
| **India-Viet Nam Defense Cooperation Agreement** | September 2016 | Ha Noi (Hanoi), Viet Nam | India and Viet Nam establish defense partnership including Indian provision of patrol vessels, defense industry cooperation, training programs, and potential access to Vietnamese port facilities (with subsequent enhancements) | High, India's Act East policy military dimension and Viet Nam's defense diversification |
| **12th Five Power Defence Arrangements (FPDA) Defence Ministers' Meeting** | May 2024 | Singapore, Singapore | Highest decision-making forum of the FPDA, bringing together defence ministers from all five member nations. Held annually on the sidelines of the Shangri-La Dialogue, this meeting sets strategic direction and approves capability enhancements for the alliance | Critical, alliance's transition to fifth-generation warfare capabilities |
| **Japan-Philippines Defense Equipment and Technology Transfer Agreement** | February 2016 | Maynila (Manila), Pilipinas (Philippines) | Bilateral agreement enabling Japanese transfer of defense equipment and technology to Philippines, including radar systems and potential patrol vessels, expanding Japan's security cooperation beyond traditional pacifist constraints | High, Japanese security policy evolution enabling defense exports |

**Code**: `MILTR_DPLY`
**Name**: Military Deployment
**Definition**: Force deployments, forward stationing, rotational presence, weapons system deployments, military infrastructure development, and basing activities. Encompasses both permanent installations and temporary deployments with strategic signaling dimensions, including deployment announcements, force arrivals/departures, infrastructure construction, and capability positioning.

**Inclusion Criteria**: 
- Military unit deployments to foreign territories or strategic locations.
- Weapons system deployments (missile batteries, advanced aircraft, naval vessels) with strategic implications.
- Military base construction or expansion in strategic locations.
- Rotational force presence under defense agreements.
- Forward-deployed capabilities with regional reach implications.

**Exclusion Criteria**: 
- Routine personnel rotations at established bases without force posture changes.
- Commercial port calls without military significance.
- Humanitarian assistance deployments unless accompanied by strategic messaging.

**Boundary Cases**: 
- Deployment duration: Code both temporary deployments (rotational forces, exercises transitioning to persistent presence) and permanent stationing as Military Deployment based on strategic significance rather than duration.
- Infrastructure vs. forces: Code military infrastructure construction (airfields, ports, facilities on artificial islands) as Military Deployment even absent immediate force stationing if infrastructure enables future operational use.
- Dual-use facilities: Code construction or enhancement of ostensibly civilian facilities (research stations, civilian airfields) as Military Deployment if credible evidence indicates military purposes or potential military use.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Chinese Military Infrastructure Development** | — | Fiery Cross Reef | China constructs military airfields, harbors, radar installations, weapons systems on artificial islands including Fiery Cross Reef, Subi Reef, Mischief Reef, transforming submerged features into military outposts (ongoing) | Critical, fundamental alteration of South China Sea military balance through fait accompli infrastructure |
| **U.S. Intermediate-Range Missile Deployment Discussions** | March 2023 | Maynila (Manila), Pilipinas (Philippines) | Following U.S. withdrawal from INF Treaty, discussions emerge regarding potential deployment of intermediate-range missile systems to Philippines under EDCA, though no confirmed deployment as of 2024 | High, signaling debate over regional missile architecture even without deployment confirmation |
| **U.S. Littoral Combat Ship Rotational Deployment** | — | Singapore, Singapore | U.S. Navy maintains rotational presence of Littoral Combat Ships at Singapore's Changi Naval Base under bilateral framework, providing persistent U.S. naval presence in Southeast Asia (ongoing) | High, enduring U.S. forward presence enabling rapid regional response |
| **Chinese Djibouti Base Establishment** | July 2017 | Jabuuti (Djibouti), Jabuuti (Djibouti) | China establishes first overseas military base in Djibouti, demonstrating expeditionary capability and affecting regional calculations regarding potential Chinese base-seeking in Indian Ocean and Pacific regions (precedent affecting regional perceptions) | High, though geographically outside ASEAN scope, influences regional base politics |
| **Vietnamese Defensive Infrastructure** | — | Spratly Islands, South China Sea | Viet Nam constructs and upgrades facilities on Vietnamese-occupied Spratly features including runways, ports, radar systems, defensive positions, maintaining territorial presence and operational capabilities (ongoing) | High, competitive militarization of disputed features by multiple claimants |

**Code**: `ARMD_INCDT`
**Name**: Armed Incident
**Definition**: Violent military confrontations including armed clashes, border skirmishes, firing incidents, casualties from military operations, armed insurgency/counterinsurgency operations with interstate dimensions, and violent encounters between state and non-state armed groups. Distinguished from non-violent military incidents (vessel encounters without shots fired, air intercepts without weapons employment) by use of lethal force and typically resulting in casualties.

**Inclusion Criteria**: 
- Exchange of fire between military/paramilitary forces.
- Casualties (killed or wounded) resulting from military operations.
- Armed attacks on military installations or personnel.
- Lethal force employment even if not resulting in casualties (shots fired, weapons employed).
- Insurgency/counterterrorism operations with cross-border dimensions or regional spillover.

**Exclusion Criteria**: 
- Accidents resulting in military casualties without hostile action.
- Training incidents causing casualties absent adversary involvement.
- Non-violent military confrontations however tense (water cannon employment, ramming without lethal intent coded as Maritime Operations).

**Boundary Cases**: 
- Gray-zone vs. armed incidents: Distinguish based on lethal force employment—water cannon, ramming, non-lethal coercion coded as Maritime Operations or other appropriate subcategory; firearms discharge, explosive employment, or lethal force coded as Armed Incident.
- Insurgency incidents: Code armed clashes between state forces and non-state armed groups as Armed Incidents if they possess interstate dimensions (cross-border operations, refugee flows, regional security implications) or occur in ASEAN member states as part of broader security environment; exclude purely internal security incidents without regional dimensions.
- Terrorism vs. insurgency: Code both terrorist attacks and insurgent operations as Armed Incidents if they involve armed groups and possess strategic regional implications.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Myanmar Military-Ethnic Armed Organization Clashes** | — | Various Border Regions | Tatmadaw engages in armed conflict with ethnic armed organizations including Karen National Union, Kachin Independence Army, and Arakan Army, generating cross-border refugee flows to Thailand and Bangladesh and regional humanitarian concerns (ongoing) | High, Myanmar internal conflict with substantial regional spillover affecting ASEAN security environment |
| **Philippine Military-Abu Sayyaf Counterterrorism Operations** | — | Mindanao/Lalawigan ng Sulu (Sulu), Pilipinas (Philippines) | Philippine Armed Forces conduct sustained counterterrorism operations against Abu Sayyaf Group and ISIS-affiliated militants in southern Philippines, involving armed clashes, casualties, and regional terrorism concerns (ongoing) | Medium-high, persistent terrorism threat affecting regional security and requiring multilateral counterterrorism cooperation |
| **Thailand-Cambodia Border Clash** | October, 2008 | Preah Vihear, Kampuchea (Cambodia) | Armed clash between Thai and Cambodian military forces near disputed Preah Vihear Temple on border results in casualties both sides, prompting ASEAN mediation and International Court of Justice involvement (precedent relevant to ASEAN conflict resolution) | High, rare interstate armed conflict within ASEAN requiring regional dispute resolution mechanisms |
| **Surabaya Family Suicide Bombings** | May 2018 | Kota Surabaya (Surabaya), Indonesia | A series of coordinated suicide bombings carried out by a single terrorist cell (JAD) against three churches and a police headquarters. The attack was notable for involving entire families, including young children, as perpetrators | Medium, ASEAN counterterrorism cooperation context and domestic security stability implications |
| **Marawi Siege** | May 2017 | Lungsod ng Marawi (Marawi), Pilipinas (Philippines) | ISIS-affiliated militants seize Marawi City prompting five-month military operation, extensive urban combat, over 1,000 casualties, and regional concerns about ISIS expansion in Southeast Asia | Critical, largest sustained urban combat in Southeast Asia in decades with regional terrorism implications |

**Code**: `AIRSPC_OPS`
**Name**: Airspace Operations
**Definition**: Military aircraft operations including air defense identification zone (ADIZ) activities, intercepts, air-to-air encounters, surveillance and reconnaissance flights, bomber deployments, and activities in contested or sensitive airspace. Encompasses both routine operational activity with strategic signaling dimensions and confrontational encounters involving military aviation.

**Inclusion Criteria**: 
- Military aircraft operations in contested or sensitive airspace.
- ADIZ incursions or activities testing air defense responses.
- Air intercepts where one country's aircraft shadows, confronts, or responds to another's.
- Strategic bomber or advanced aircraft deployments with regional signaling.
- Reconnaissance or surveillance flights with strategic intelligence dimensions.

**Exclusion Criteria**: 
- Routine civil aviation operations even if involving state-owned airlines.
- Military transport flights without strategic signaling dimensions.
- Internal air defense training without international dimensions.

**Boundary Cases**: 
- ADIZ vs. sovereign airspace: Code all ADIZ-related activities as Airspace Operations regardless of whether they occur in internationally recognized sovereign airspace or claimed ADIZ zones, as ADIZ disputes themselves constitute strategic contestation.
- Combined air-sea operations: Code incidents involving both air and maritime components based on which dimension drives the incident; if roughly equal, select based on which capability initiates contact or represents primary operational focus.
- Close calls vs. routine operations: Code air encounters as Airspace Operations if they involve proximity closer than safe operating distances, if intercepts occur, or if official protests or statements follow; exclude routine operations maintaining safe distances without interaction.

**Anchoring Examples**: 
| Event | Date | Location | Definition | Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Chinese Military Aircraft Incursions Near Taiwan** | — | Taiwan Strait ADIZ | People's Liberation Army Air Force conducts frequent sorties near Taiwan including crossing median line of Taiwan Strait, with regional implications for Southeast Asian security calculations regarding China's growing air power and potential conflict scenarios (ongoing) | High, demonstration of Chinese military capability affecting regional strategic environment |
| **U.S. Strategic Bomber Flights** | — | South China Sea | U.S. Air Force conducts B-52 or B-1 bomber flights over South China Sea, sometimes coordinating with regional partners, asserting rights to overflight international airspace and signaling regional security commitments (periodic) | High, U.S. power projection demonstration and alliance reassurance |
| **Russian Military Aircraft in Asian Airspace** | — | Eastern Asian ADIZ | Russian military aircraft conduct long-range flights through Asian airspace including near Japan, Korea, and potentially ASEAN airspace, prompting regional air defense responses and demonstrating reach (periodic) | Medium, Russian military presence maintenance in Asia-Pacific beyond primary European focus |
| **Singapore-Malaysia Airspace Dispute** | December 2018 | Bandaraya Pasir Gudang (Pasir Gudang), Johor Darul Ta'zim (Johor), Malaysia Airspace | Malaysia objects to Singapore's publication of instrument landing system procedures for Seletar Airport, claiming infringement on Malaysian airspace, prompting diplomatic tensions and temporary restrictions | Medium, rare bilateral dispute between normally cooperative ASEAN neighbors over technical airspace issues |
| **Vietnamese Airspace Surveillance Operations** | — | South China Sea | Vietnamese Air Force conducted surveillance flight over disputed waters, tracking Chinese construction activities on artificial islands | Medium, continued monitoring by smaller power's employment of available air capabilities |

---

### Actor Typology and Attribution Framework

### Actor Category Definitions
 
**Code**: `ACTOR`
**Name**: Actor Category Definitions

**Subcategories**: 
**Code**: `STATE_MLITR`
**Name**: State Military
**Definition**: Regular armed forces of nation-states including armies, navies, air forces, marine corps, and unified military commands operating under formal military command structures and national defense ministries. Distinguished from paramilitary forces by formal military status, combatant legal status under international law, and conventional military organizational structures.

**Organisational Scope**: 
- National military services and branches (Chinese People's Liberation Army, U.S. Indo-Pacific Command, Philippine Armed Forces).
- Theater or regional military commands (PLA Southern Theater Command, U.S. Seventh Fleet).
- Specialized military units if operating as part of regular military structure (special operations forces, military intelligence units).

**Exclusion Criteria**: 
- Coast guard or maritime law enforcement even if militarized (code as State Paramilitary).
- Intelligence agencies with civilian command chains (code as Government Civilian).
- Police or internal security forces (code as State Paramilitary if conducting border/maritime operations with regional dimensions).

**Anchoring Examples**: 
- Zhongguo Renmin Jiefangjun Haijun (People's Liberation Army Navy, Chinese naval forces)
- U.S. Indo-Pacific Command (U.S. military unified combatant command)
- Hukbong Dagat ng Pilipinas (Philippine Navy, Philippine military naval service)
- Tatmadaw (Myanmar Royal Armed Forces, Myanmar military forces)
- Kong Thap Thai (Royal Thai Armed Forces, Thai military)

**Code**: `STATE_PARMLITR`
**Name**: State Paramilitary
**Definition**: State-controlled or state-affiliated forces with military capabilities but distinct organizational status from regular military, including coast guards, maritime law enforcement, border guards, gendarmerie-type forces, and state-coordinated militia operating under civilian agency command but performing quasi-military functions particularly in maritime law enforcement and border security.

**Organisational Scope**: 
- Coast guard and maritime law enforcement agencies (China Coast Guard, Philippine Coast Guard, Viet Nam Marine Police).
- People's Armed Police or internal security forces when conducting external operations.
- Maritime militia with state coordination (Chinese People's Armed Forces Maritime Militia).
- Border guard forces with paramilitary capabilities.

**Exclusion Criteria**: 
- Regular military forces regardless of law enforcement mission (naval vessels conducting law enforcement operations coded as State Military).
- Purely civilian law enforcement without maritime/border/external dimensions.
- Non-state militia lacking government coordination.

**Anchoring Examples**: 
- Zhongguo Haijingju (China Coast Guard, Chinese maritime law enforcement, operates under China Coast Guard Administration)
- Zhongguo Haishang Minbing (People's Armed Forces Maritime Militia, Chinese fishing vessels with state coordination performing maritime missions)
- Tanod Baybayin ng Pilipinas (Philippine Coast Guard, Philippine maritime law enforcement, distinct from Philippine Navy)
- Canh sat bien Viet Nam (Viet Nam Coast Guard, Vietnamese maritime law enforcement)
- Bakamla (Indonesian Maritime Security Agency, coordinating body for Indonesian maritime enforcement)

**Code**: `GOV_CIVL`
**Name**: Government Civilian
**Definition**: Civilian government agencies and officials conducting foreign policy, intelligence operations, diplomatic functions, or civilian-led national security activities. Distinguished from military/paramilitary by civilian organizational structures and policy rather than operational functions, though intelligence agencies may conduct operations similar to military intelligence units.

**Organisational Scope**: 
- Foreign ministries and diplomatic services (Ministry of Foreign Affairs entities).
- Intelligence agencies with civilian leadership (though attribution often limited).
- National security councils and inter-agency policy coordinating bodies.
- Government spokespeople and official communications representing state positions.

**Exclusion Criteria**: 
- Military intelligence units operating within defense ministry structures (code as State Military).
- State-owned enterprises unless explicitly conducting government-directed political operations.
- Individual politicians unless speaking in official government capacity.

**Anchoring Examples**: 
- Zhonghua Renmin Gongheguo Waijiaobu (Chinese Ministry of Foreign Affairs, diplomatic policy formulation and official statements)
- U.S. State Department (American diplomatic agency)
- Kagawaran ng Ugnayang Panlabas (Philippine Department of Foreign Affairs, Philippine diplomatic agency)
- ASEAN Secretariat when conducting diplomatic functions (though also International Organization)

**Code**: `NSTATE_ARMD_GRP`
**Name**: Non-State Armed Group
**Definition**: Armed organizations operating outside formal state military structures including insurgent groups, ethnic armed organizations, secessionist movements, and organized armed opposition to governments. Distinguished from terrorist organizations (which may overlap) by political objectives and territorial control aspirations, and from criminal networks by primarily political rather than economic motivations.

**Organisational Scope**: 
- Ethnic armed organizations in Myanmar (Karen National Union, Kachin Independence Army, Arakan Army).
- Separatist movements with armed components (Moro Islamic Liberation Front in Philippines historically, though peace process transformed status).
- Opposition armed groups in civil conflicts (People's Defense Forces in Myanmar post-2021 coup).

**Exclusion Criteria**: 
- Terrorist organizations primarily motivated by ideological rather than territorial-political objectives (code separately if you establish separate category, or include here with notation).
- Criminal organizations even if armed (code as Criminal Network).
- Pro-government militia (code as State Paramilitary if government-coordinated).

**Anchoring Examples**: 
- Kayin Amyotha Ahnye (Karen National Union/Karen National Liberation Army, ethnic armed organization in Myanmar)
- Wunpawng Mungdan Shanglawt Hpyen Dap (Kachin Independence Army, ethnic armed organization in Myanmar's Kachin State)
- Arakha Tatdaw (Arakan Army, ethnic armed organization in Myanmar's Rakhine State)
- Amyotha Nyi-nyut-ye Ah-so-ya (National Unity Government/People's Defense Forces, opposition to Myanmar military junta post-2021)
      
**Code**: `CRIMNL_NTWRK`
**Name**: Criminal Network
**Definition**: Organized criminal syndicates and networks engaged in transnational crime with regional security implications including drug trafficking, human trafficking, illegal wildlife trade, piracy, and organized smuggling operations. Distinguished from armed groups by primarily economic rather than political motivations and from state actors by lack of government authority.

**Organisational Scope**: 
- Drug trafficking organizations operating transnationally.
- Human trafficking and migrant smuggling networks.
- Piracy operations in regional waters (Malacca Strait pir.acy, Sulu Sea kidnapping-for-ransom)
- Organized illegal wildlife trade networks.

**Exclusion Criteria**: 
- Individual criminal acts without organized network structures.
- State-sponsored criminal activity (government smuggling or sanctions evasion coded under appropriate state actor category).
- Terrorist financing networks (code under non-state armed group or terrorist organization if separate category established).

**Anchoring Examples**: 
- Piracy syndicates operating in Malacca Strait or Sulu Sea
- Transnational drug trafficking networks operating through Mekong region
- Human trafficking networks exploiting Ruáingga (Rohingya) refugees
- Illegal wildlife trade networks (though often incidents focus on state enforcement responses)
      
**Code**: `PRVT_SEC`
**Name**: Private Security
**Definition**: Private military and security companies, commercial security providers, and private armed contractors operating in regional contexts. Distinguished from state forces by commercial corporate structure and contractual relationships, though may operate on behalf of governments or in close coordination with state actors.

**Organisational Scope**: 
- Private military companies providing security services.
- Maritime private security contractors aboard commercial vessels.
- Corporate security entities if involved in incidents with regional security dimensions.

**Exclusion Criteria**: 
- Unarmed private security or commercial security without military dimensions.
- Private companies providing non-security services even if government-contracted.

**Note**: This actor type may have limited representation in the database as private military companies play smaller roles in East/Southeast Asian contexts compared to other regions, but category remains available for completeness.

**Code**: `INTL_ORG`
**Name**: International Organisation
**Definition**: Multilateral intergovernmental organizations including regional institutions, global governance bodies, and international tribunals. Distinguished from state actors by representing collective member state positions and from non-governmental organizations by official intergovernmental status.

**Organisational Scope**: 
- ASEAN Secretariat and ASEAN institutional mechanisms.
- United Nations entities with regional operations or relevance.
- International tribunals (Permanent Court of Arbitration, International Court of Justice when adjudicating regional disputes).
- Regional organizations (ASEAN Regional Forum, East Asia Summit institutional structures).

**Exclusion Criteria**: 
- Non-governmental organizations lacking official intergovernmental status.
- Informal groupings without institutional structures (Quad treated as collective of member states rather than organization).

**Anchoring Examples**: 
- ASEAN Secretariat (administrative body of Association of Southeast Asian Nations)
- United Nations (when UN entities conduct operations or issue reports relevant to regional security)
- Permanent Court of Arbitration (when adjudicating South China Sea arbitration)
- Mekong River Commission (institutional body governing Mekong water resources with security implications)

**Code**: `OTHER`
**Name**: Other
**Definition**: Residual category for actors not fitting primary classifications including hybrid entities, ambiguous organizations, or novel actor types emerging in evolving security environment.

**Usage**: Minimize use of "Other" category through careful application of primary categories; when necessary, provide detailed description explaining why primary categories prove inadequate and specifying actor nature.

#### Attribution Confidence Protocols

**Code**: `ATTR_CONF`
**Name**: Attribution Confidence Protocols

**Subcategories**: 
**Code**: `CONFRM`
**Name**: Confidence Level 1: Confirmed
**Definition**: Attribution or factual claim supported by official government acknowledgment, incontrovertible documentary evidence, or multiple independent primary sources with direct knowledge providing consistent accounts.

**Evidence Standards**: 
- Official government press releases, ministry statements, or military announcements acknowledging actor involvement.
- Firsthand journalistic reporting from credible outlets with reporters directly observing incidents.
- Multiple (3+) independent sources including primary sources (government officials, military personnel, direct witnesses) providing consistent accounts.
- Photographic or video evidence definitively identifying actors (military unit markings, vessel identification numbers, official insignia clearly visible).
- Legal proceedings or tribunal findings establishing facts (arbitration awards, court judgments).

**Anchoring Examples**: 
| Event | Definition | Confidence |
| :--- | :--- | :--- |
| **U.S. FONOPs** | U.S. Navy press releases explicitly announcing operations, vessel identifications provided, routes documented | Confirmed |
| **ASEAN Summit outcomes** | Official ASEAN communiqués, host country statements, multiple participating governments' readouts providing consistent accounts | Confirmed |
| **Armed incidents with acknowledged casualties** | Government announcements of military casualties, official death tolls, military funerals | Confirmed |

**Code**: `SUS`
**Name**: Confidence Level 2: Suspected
**Definition**: Attribution or factual claim supported by strong circumstantial evidence, credible secondary sources, or informed analysis from established experts/institutions, but lacking official confirmation or incontrovertible primary evidence. Represents high probability based on available evidence but retains uncertainty acknowledging incomplete information.

**Evidence Standards**: 
- Credible think tank analysis attributing incidents based on circumstantial evidence (vessel tracking data, operational patterns, modus operandi matching known actors).
- News reporting from reputable outlets citing unnamed official sources or informed analysts.
- Technical analysis (satellite imagery interpretation, vessel automatic identification system data analysis) by recognized experts.
- Pattern recognition suggesting state involvement based on capabilities, motivations, and operational signatures.
- Single primary source account lacking corroboration but from highly credible source.

**Anchoring Examples**: 
| Event | Definition | Confidence |
| :--- | :--- | :--- |
| **Zhongguo Haishang Minbing (People's Armed Forces Maritime Militia) attribution** | Vessels lack official markings but exhibit coordination, identical characteristics, operate in patterns suggesting state direction, identified by think tank analysis (CSIS AMTI, CNAS) | Suspected (elevated to Confirmed if official Chinese statements acknowledge or multiple primary sources document coordination) |
| **Cyber operations** | Malware analysis, infrastructure attribution, modus operandi matching known state-sponsored groups, cybersecurity firm attribution | Suspected (rarely reaches Confirmed without government official attribution) |
| **Informal economic restrictions** | Customs delays targeting specific country exporters documented by business associations, temporal correlation with political disputes, but no official policy announcement | Suspected |

**Code**: `3RD_PARTY`
**Name**: Level 3: Third-Party Attribution
**Definition**: Attribution made by external credible entity (foreign government, international organization, established research institution) but not confirmed by the attributed actor or definitive independent evidence. Represents claims accepted by significant portions of expert community but remaining contested or unverified by some parties.

**Evidence Standards**: 
- Foreign government official statements attributing incidents to specific actors (U.S. government attributing cyber operations to Chinese state-sponsored groups).
- International organization findings or reports attributing responsibility (UN panels of experts, Human Rights Watch investigative reports).
- Tribunal or court findings when defendant contests or does not participate (arbitration awards where respondent rejects jurisdiction).
- Established think tank definitive attribution reports synthesizing multiple evidence types.

**Anchoring Examples**: 
| Event | Definition | Confidence |
| :--- | :--- | :--- |
| **Cyber operations attributed by U.S. government to Chinese state-sponsored actors** | U.S. official statements naming PLA units, Department of Justice indictments | Third-Party Attribution (unless China acknowledges, which rarely occurs) |
| **South China Sea Arbitral Tribunal findings** | Tribunal ruled on Philippine claims against China, China rejected jurisdiction and findings | Third-Party Attribution for specific factual findings China contests |
| **Human rights violation attributions** | International human rights organizations attribute atrocities to specific military units based on investigations, implicated government denies | Third-Party Attribution |

**Note**: When insufficient information exists to determine confidence level, default to "Suspected" rather than "Contested" if single plausible attribution exists based on circumstantial evidence; reserve "Contested" for situations with genuine competing claims from credible sources rather than mere absence of confirming evidence.

**Code**: `CNTEST`
**Name**: Confidence Level 4: Contested
**Definition**: Significant disagreement exists among credible sources regarding attribution or factual claims, with multiple competing accounts from sources of roughly comparable credibility. Represents genuine uncertainty where available evidence permits multiple reasonable interpretations or where state actors provide conflicting official accounts.

**Evidence Standards**: 
- Multiple credible sources providing materially different accounts of actor involvement or incident facts.
- Official government statements directly contradicting each other on factual questions.
- Expert analysis divided on attribution with competing schools of thought presenting reasonable arguments.
- Propaganda environments where information warfare obscures factual determination.

**Anchoring Examples**: 
| Event | Definition | Confidence |
| :--- | :--- | :--- |
| **Incidents in information-contested environments** | Myanmar civil conflict incidents where Tatmadaw, ethnic armed organizations, and opposition provide contradictory accounts, independent verification impossible | Contested |
| **Border incidents with competing territorial claims** | Incidents on disputed borders where both sides claim self-defense responding to other's provocation, no independent witnesses = | Contested |
| **Ambiguous gray-zone operations** | Incidents potentially involving state actors but also potentially private actors without state coordination, insufficient evidence determining state involvement | Contested |

**Note**: When insufficient information exists to determine confidence level, default to "Suspected" rather than "Contested" if a single plausible attribution exists based on circumstantial evidence; reserve "Contested" for situations with genuine competing claims from credible sources rather than mere absence of confirming evidence.

#### Attribution Coding Decision Trees

**Code**: `DCISN_TREE`  
**Name**: Attribution Coding Decision Trees

**Decision Tree 1: State Military vs. State Paramilitary Distinction**
**Code**: `MLITR_PARMLITR`

- **Is the actor operating under formal military command structure (defense ministry, military chief of staff chain of command)?**
  - If **YES** → **State Military**
  - If **NO** → **Is the actor a coast guard, maritime law enforcement, border guard, or internal security force?**
    - If **YES** → **State Paramilitary**
    - If **NO** → **Does the actor possess military capabilities (armed vessels, weapons systems) but operate under civilian agency command?**
      - If **YES** → **State Paramilitary**
      - If **NO** → **Consider Government Civilian or Other depending on actor nature**

**Decision Tree 2: Non-State Armed Group vs. Criminal Network Distinction**  
**Code**: `NSTATE_ARMD_GRP_CRIMNL_NTWRK`

- **Does the organization's primary stated objective involve political goals (autonomy, self-determination, government change, territorial control)?**
  - If **YES** → **Non-State Armed Group**
  - If **NO** → **Does the organization primarily engage in profit-motivated criminal activity (drug trafficking, smuggling, kidnapping-for-ransom)?**
    - If **YES** → **Criminal Network**
    - If **NO** → **Does the organization combine political and criminal motivations or operate in a gray area?**
      - Evaluate based on the following conditions:
        - If **political objectives predominate or organization controls territory** → **Non-State Armed Group**
        - If **criminal profit predominates and lacks political control aspirations** → **Criminal Network**
        - Otherwise → **Other (provide detailed description)**

**Decision Tree 3: Attribution Confidence Assignment** 
**Code**: `ATTR_CONF`

- **Does official government acknowledge actor involvement through press releases, statements, or military announcements?**
  - If **YES** → **Confirmed** (proceed to verify consistency with other evidence)
  - If **NO** → **Do multiple (3+) independent credible sources provide consistent accounts of actor involvement?**
    - If **YES** → **Confirmed**
    - If **NO** → **Does strong circumstantial evidence (operational patterns, technical analysis, capabilities matching) suggest specific actor involvement?**
      - If **YES** → **Suspected**
      - If **NO** → **Has credible third party (foreign government, international organization, established institution) made definitive attribution?**
        - If **YES** → **Third‑Party Attribution**
        - If **NO** → **Do multiple credible sources provide materially conflicting accounts of actor involvement?**
          - If **YES** → **Contested**
          - If **NO** → **If a single plausible attribution exists with minimal evidence, code as Suspected; if no reasonable attribution is possible, consider excluding the incident or coding with extensive notes explaining uncertainty**

---

### Multi-Dimensional Impact Assessment Framework

#### Military Impact Dimensions

**Code**: `MLITR`  
**Name**: Military Impact Dimensions

**Quantifiable Metrics**:
| Casualties | Measurement | Source Standards | Coding Protocols | Missing Data |
| :--- | :--- | :--- | :--- | :--- |
| **Killed** | `INTEGER`, fatalities directly resulting from incident | Official government casualty announcements preferred; credible news reporting from outlets with access to official sources or direct reporting acceptable; human rights organization documentation acceptable for incidents where governments provide no figures or contested figures | Use minimum confirmed figures when ranges provided; if sources disagree on figures, use most credible source (government official statements > established news outlets > advocacy organizations) and note discrepancy in event notes | `NULL` (not zero) for incidents where casualty figures unknown or not applicable (diplomatic meetings, economic agreements) |
| **Wounded** | `INTEGER`, injured persons requiring medical treatment | Parallel to fatalities, official announcements preferred | Distinguish wounded requiring hospitalization from minor injuries if sources permit. When not specified, include all reported injuries. Note if figures represent initial reports subject to revision | `NULL` for non-applicable incidents |
| **Displaced** | `INTEGER`, persons forcibly displaced (internally displaced persons, refugees) directly attributable to incident | UNHCR figures, government statistics, credible humanitarian organization reports | Code displacement only when sources explicitly link displacement to specific incident. For ongoing conflicts, code displacement associated with particular escalations or campaigns rather than cumulative figures across all incidents | `NULL` for incidents not generating displacement |

**Qualitative Assessments**:
**Definition**: Given that most ASEAN security incidents in the 2016-present timeframe involve zero casualties (diplomatic engagements, economic measures, non-lethal gray-zone coercion), military impact assessment extends beyond fatality counts to operational and strategic military dimensions (captured in event description and strategic significance rather than separate coded field).

**Military Operational Impact**:
- Force posture changes (deployments, redeployments, readiness level alterations).  
- Military infrastructure development or damage.  
- Operational tempo changes (increased patrols, exercises, surveillance).
- Capability demonstrations (weapons systems employment, new technology displays).

#### Economic Impact Dimensions

**Code**: `ECON`
**Name**: Economic Impact Dimensions

**Quantifiable Metrics**:
| Impact | Measurement | Measurement Approaches | Source Standards | Coding Protocols | Missing Data |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Economic Impact (USD)** | `NUMERIC(15,2)`, storing estimated economic consequences in U.S. dollars | • **Trade agreements**: Estimated bilateral trade value affected by agreement provisions (tariff eliminations, market access); use government estimates from official impact assessments or economic modeling studies by credible institutions.<br>• **Infrastructure financing**: Project value as stated in financing agreements or credible media reporting.<br>• **Economic coercion**: Estimated trade value affected by restrictions, calculated from prior‑year trade statistics for affected products/sectors; use conservative estimates.<br>• **Sanctions**: Estimated economic costs based on targeted asset values, affected trade volumes, or economic modeling by think tanks/academic institutions. | Official government figures (finance ministry, trade ministry, statistical agencies) preferred; multilateral development bank project documentation; credible economic think tank analyses; business press reporting citing company or government sources. | Convert all figures to USD using exchange rates contemporaneous with incident; for agreements with multi‑year impacts, code initial year implementation value or total project value with notation in description; prefer conservative estimates when ranges provided. | `NULL` for incidents without quantifiable economic dimensions (most diplomatic signaling, military incidents without economic consequences). |

**Qualitative Dimension**:
- Supply chain disruption or reconfiguration.
- Investment climate effects.
- Economic statecraft effectiveness (did coercive measures achieve stated objectives?).
- Market access implications.
- Technology transfer or denial.

#### Political Impact Dimensions

**Code**: `POLTIC`
**Name**: Political Impact Dimensions
**Definition**: This dimension assesses bilateral or multilateral relationship quality changes attributable to incidents, using ordinal categories capturing diplomatic relationship trajectories.

**Subcategories**:
**Code**: `IMPRV`
**Name**: Improved
**Definition**: Incident generates measurable improvement in bilateral/multilateral relationship quality through enhanced cooperation, tension reduction, or positive diplomatic momentum.

**Indicators**: 
- Official statements characterizing relationship elevation.
- New cooperation mechanisms established.
- Prior disputes resolved or de-escalated.
- Increased high-level engagement frequency.

**Anchoring Examples**:
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **U.S.-ASEAN Special Summit** | May 2022 | Washington, D.C., United States | Elevated relationship to Comprehensive Strategic Partnership | Improved |
| **China-Philippines bilateral agreements** | November 2018 | Maynila (Manila), Philippines | Following years of tension, summit generates 29 cooperation agreements improving relations | Improved |
| **ASEAN-China dialogue reducing South China Sea tensions (hypothetical if occurred)** | — | — | Demonstrable de-escalation following diplomatic engagement | Improved |

**Code**: `STBL`
**Name**: Stable
**Definition**: Incident occurs within context of stable relationship without generating significant positive or negative diplomatic consequences, or positive and negative effects roughly balance.

**Indicators**: 
- Routine diplomatic engagement without relationship status changes.
- Incidents managed through established mechanisms without escalation.
- No significant official rhetoric changes.

**Anchoring Examples:**
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **55th ASEAN Foreign Ministers' Meeting** | November 2022 | Phnom Penh, Cambodia | Regular institutionalized engagement maintaining stable relationships | Stable |
| **Brunei–Malaysia maritime encounter near Limbang** | March 2020 | Limbang, Negeri Sarawak (Sarawak), Malaysia | A Malaysian vessel was reported to have entered Brunei’s claimed waters. Minor incident creating brief tension followed by return to normal | Stable |
| **Defense cooperation agreement renewals** | — | — | Continuation of existing arrangements without major changes | Stable |

**Code**: `DETRIOR`
**Name**: Deteriorated
**Definition**: Incident generates measurable worsening of bilateral/multilateral relationship quality through increased tensions, reduced cooperation, or negative diplomatic momentum.

**Indicators**: 
- Official protest statements.
- Diplomatic démarches.
- Reduced engagement frequency.
- Cooperation mechanisms suspended.
- Public rhetorical tensions, but relationships remain intact with diplomatic channels functioning.

**Anchoring Examples**:
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Chinese maritime militia swarming incidents** | September 2023 | South China Sea | Generate Philippine protests, diplomatic tensions, but no relationship rupture | Deteriorated |
| **Economic coercion incidents** | — | — | Informal restrictions generate bilateral tensions and protests | Deteriorated |
| **57th ASEAN Foreign Ministers' Meeting** | July 2024 | Viang Chan (Vientiane), Lao PDR (Laos) | ASEAN disunity over South China Sea statements. Failure to achieve consensus generates intra-ASEAN tensions | Deteriorated |

**Code**: `RUPTR`
**Name**: Ruptured 
**Definition**: Incident generates severe relationship breakdown including diplomatic channel suspensions, ambassador recalls, cooperation mechanism terminations, or moves toward adversarial postures.

**Indicators**: 
- Ambassador recall or expulsion.
- Diplomatic relations suspension or downgrade.
- Comprehensive cooperation cessation.
- Official rhetoric characterizing relationship as adversarial.
- Severing of institutional mechanisms.

**Anchoring Examples**:
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Myanmar coup 2021 response by some ASEAN members** | March 2021 | Nay Pyi Taw (Naypyidaw), Myanmar | Singapore ambassador recall, cooperation suspensions | Ruptured (for specific bilateral relationships, not all ASEAN-Myanmar relations) |
| **Hypothetical major armed clash** | — | — | If theoretical interstate armed conflict occurred, could generate relationship rupture | Ruptured |
| **Severe diplomatic crises (rare in contemporary ASEAN)** | — | — | Complete breakdown of diplomatic engagement | Ruptured |

**Coding Protocols**:
- Assess political impact relative to pre-incident relationship baseline; same incident may generate different impact assessments for different bilateral dyads (e.g., China-Philippines maritime incident may deteriorate China-Philippines relations while leaving China-Vietnam relations stable).
- Use `NULL` for incidents lacking clear bilateral/multilateral political relationship dimensions (internal security incidents, purely technical agreements, unilateral actions not eliciting partner responses).
- For multilateral incidents (ASEAN summits, regional forums), assess primary political trajectory or code as Stable if maintaining status quo represents the outcome.
- Note in event description which specific bilateral relationships the political impact assessment references if incident involves multiple countries with varying relationship effects.

**Evidence Standards**:
- Official government statements characterizing relationship status.
- Diplomatic engagement frequency changes measurable through meeting counts.
- Cooperation mechanism status (established, suspended, terminated).
- Media analysis by credible regional affairs specialists interpreting relationship trajectories.
- Comparative historical context (is current tension level higher/lower than prior periods?).

#### Legal‑Normative Impact Dimensions

**Code**: `LGL_NORMTV`  
**Name**: Legal‑Normative Impact Dimensions  
**Definition**: This dimension evaluates incident implications for international law, regional norms, and rules‑based order, assessing whether incidents affirm, test, or violate established legal frameworks and normative expectations.

**Subcategories**:
**Code**: `AFFRM` 
**Name**: Affirming
**Definition**: Incident demonstrates respect for international law, strengthens rules‑based order, or establishes positive precedent for norm compliance.

**Indicators**:  
- Explicit citation of international law in justifying actions.
- Compliance with tribunal rulings.
- Respect for UNCLOS provisions.
- Peaceful dispute resolution through legal mechanisms.
- Transparency consistent with international standards.

**Anchoring Examples**:
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Philippines bringing South China Sea arbitration case** | July 2016 | Den Haag (The Hague), Nederland (Netherlands) | Using legal mechanisms for dispute resolution (ongoing) | Affirming |
| **U.S. FONOPs explicitly citing UNCLOS Article 87 freedom of navigation** | May 2016 | Fiery Cross Reef | Asserting international law provisions | Affirming |
| **49th ASEAN Foreign Ministers' Meeting (AMM)** | July 2016 | Viang Chan (Vientiane), Lao PDR (Laos) | ASEAN statements reaffirming commitment to UNCLOS and peaceful dispute resolution | Affirming |
| **EU‑Malaysia Framework Agreement on Partnership and Cooperation (PCA)** | April 2016 | Wilayah Persekutuan Putrajaya (Putrajaya), Malaysia | Bilateral agreements incorporating international legal standards | Affirming |

**Code**: `NUTRL` 
**Name**: Neutral
**Definition**: Incident neither significantly strengthens nor undermines international legal norms; operates in areas where international law provides limited guidance or where legal implications remain ambiguous.

**Indicators**:  
- Actions within clearly permitted scope of international law without precedent‑setting dimensions.
- Technical implementation of existing legal obligations.
- Activities in legal gray areas where multiple interpretations exist.

**Anchoring Examples**:
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Indonesia‑Singapore Eagle Indopura Exercise** | September 2021 | Laut Natuna (Natuna Sea), Indonesia | Routine bilateral defense cooperation. Within sovereign state rights, no particular legal implications | Neutral |
| **Regional Comprehensive Economic Partnership (RCEP)** | November 2020 | Virtual | Economic agreements following standard treaty practice | Neutral |
| **44th and 45th ASEAN Summits** | October 2024 | Viang Chan (Vientiane), Lao PDR (Laos) | Diplomatic engagements without legal dimensions | Neutral |
| **ASEAN Solidarity Exercise (ASEX‑01N)** | September 2023 | Laut Natuna (Natuna Sea)/Kota Batam (Batam), Indonesia | Military exercises in clearly sovereign territory or uncontested international waters | Neutral |

**Code**: `TEST` 
**Name**: Testing
**Definition**: Incident probes boundaries of international law, challenges interpretations without outright violations, or operates in legal gray zones pushing normative limits while maintaining plausible legal justifications.

**Indicators**:  
- Actions with contested legal interpretations.
- Exploiting ambiguities in international law.
- Challenging but not outright rejecting legal frameworks.
- “Salami‑slicing” incrementalism testing response thresholds.

**Anchoring Examples**:
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Chinese artificial island construction** | — | South China Sea | Claims sovereignty over features, builds installations; legal status contested under UNCLOS but China asserts sovereignty rights (ongoing) | Testing |
| **Chinese historic rights claims reaffirmation in South China Sea** | July 2016 | South China Sea | Claims based on contested legal theories not clearly supported by UNCLOS | Testing |
| **Coast guard operations in contested EEZs** | February 2024 | Scarborough Shoal | Asserting jurisdiction in areas where claims overlap, operating within claimed rights but contested by others | Testing |
| **Dual‑use infrastructure in disputed areas** | March 2017 | Fiery Cross Reef/Mischief Reef | Military facilities on features with contested sovereignty | Testing |

**Code**: `VIOLTN`
**Name**: Violating
**Definition**: Incident constitutes clear violation of international law, explicit rejection of legal rulings, or egregious breach of fundamental norms (use of force prohibitions, sovereignty principles, human rights law).

**Indicators**:  
- Actions directly contravening tribunal rulings.
- Violations of UNSC resolutions.
- Use of force absent self‑defense justification.
- Rejection of binding international legal obligations.
- Widespread international condemnation citing legal violations.

**Anchoring Examples**:
| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **China's rejection of 2016 Arbitral Tribunal ruling** | July 2016 | Den Haag (The Hague), Nederland (Netherlands) | Explicit refusal to accept binding legal decision under UNCLOS | Violating (regarding rejection of legal process, though China claims tribunal lacked jurisdiction) |
| **Myanmar military coup 2021** | February 2021 | Nay Pyi Taw (Naypyidaw), Myanmar | Violation of constitutional order, followed by violence against civilians violating international humanitarian law and human rights law | Violating |
| **Hypothetical use of force without self‑defense justification** | — | — | Would violate UN Charter Article 2(4) prohibition on use of force | Violating |
| **Major armed attacks on civilians by state forces** | — | — | Violations of international humanitarian law | Violating |

**Coding Protocols**:
- Assess legal‑normative implications based on international law standards (UNCLOS, UN Charter, customary international law) and established regional norms (ASEAN Treaty of Amity and Cooperation, ASEAN Charter provisions).
- Distinguish between contested legal interpretations (Testing) and clear violations where international legal consensus exists (Violating); err toward Testing category when genuine legal ambiguity exists.
- Use NULL for incidents lacking international legal dimensions (purely domestic matters, technical cooperation without normative implications).
- Note in event description specific legal frameworks or norms implicated (UNCLOS Articles, UN Charter provisions, regional agreements).

**Evidence Standards**:
- International legal expert analysis from academic institutions or established think tanks.
- Statements by international law scholars in credible publications.
- International tribunal or court rulings and reasoning.
- Official government statements citing international law provisions.  
- UN or regional organization reports assessing legal dimensions. 
- Comparative state practice (are other states acting similarly, suggesting accepted interpretation? Or is action widely condemned, suggesting violation?).

#### Strategic Significance Assessment 
**Code**: `STRTGY`
**Name**: This composite dimension synthesizes military, economic, political, and legal‑normative impacts with strategic context to assess overall incident importance for regional security dynamics. Unlike specific impact dimensions measuring particular consequences, strategic significance evaluates incidents' importance for broader power competition, alliance dynamics, normative trajectories, and potential escalation risks.

**Subcategories**:
**Code**: `LOW`
**Name**: Low
**Definition**: Incident possesses limited implications beyond immediate bilateral context, represents routine interaction pattern without novelty or escalation, generates minimal regional attention, and unlikely to influence broader strategic trajectories.

**Indicators**: Limited media coverage, absence of significant official reactions beyond immediate parties, represents continuation of established patterns, affects narrow issue area without spillover implications.

**Anchoring Examples**:
- Routine diplomatic working‑level meetings without substantive outcomes
- Small‑scale economic agreements of limited value
- Minor technical cooperation arrangements
- Isolated low‑intensity incidents quickly resolved

**Code**: `MID`
**Name**: Medium
**Definition**: Incident possesses notable implications for bilateral relationships or specific issue areas, may establish incremental precedents, generates regional awareness, but does not fundamentally alter strategic dynamics or require major policy responses.

**Indicators**:  
Moderate media attention, official statements by involved parties and some regional states, represents meaningful development in specific relationship or issue area, may influence related incidents but limited broader systemic implications.

**Anchoring Examples**:
- Bilateral ministerial meetings generating substantive cooperation agreements
- Economic coercion incidents generating protests but not prompting major policy shifts
- Maritime incidents prompting diplomatic responses but no operational escalation
- Defense cooperation agreements enhancing specific bilateral relationships without fundamentally shifting regional balance
- Regional forum meetings with tangible but incremental outcomes

**Code**: `HI`
**Name**: High
**Definition**: Incident significantly affects bilateral or multilateral relationships, establishes important precedents, generates substantial regional attention and policy responses, influences strategic calculations of multiple actors, but does not represent transformational shifts or crisis‑level developments.

**Indicators**: Extensive media coverage including analysis from regional security specialists, official reactions from multiple regional states, policy adjustments by affected parties, influences related issue areas or bilateral relationships, cited in strategic planning discussions.

**Anchoring Examples**:
- Major defense cooperation agreements substantially enhancing alliance capabilities (EDCA expansion)
- Large‑scale economic agreements reshaping trade architecture (RCEP signing)
- Significant armed incidents generating casualty concerns and escalation risks (Myanmar conflict escalations affecting border regions)
- Diplomatic initiatives establishing new institutional mechanisms (ASEAN Outlook on Indo‑Pacific)
- Maritime incidents involving major powers with potential escalation implications (China‑U.S. vessel encounters)
- Economic coercion campaigns affecting significant trade values and prompting diversification strategies

**Code**: `CRTCL`
**Name**: Critical
**Definition**: Incident fundamentally affects regional security architecture, represents transformational developments, generates crisis‑level attention requiring high‑level policy responses, establishes major precedents with systemic implications, or possesses potential for major escalation or conflict.

**Indicators**: Sustained intensive international media coverage, responses from senior leadership across multiple countries, emergency diplomatic engagement, policy reassessments and strategic reviews, long‑term implications for regional order, referenced as watershed moments in strategic analyses.

**Anchoring Examples**:

| Event | Date | Location | Definition | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Myanmar military coup** | February 2021 | Nay Pyi Taw (Naypyidaw), Myanmar | Fundamental disruption of ASEAN member political system, humanitarian crisis, regional institutional challenge to ASEAN consensus norms | Critical |
| **AUKUS partnership announcement** | September 2021 | Washington, D.C., United States | Major strategic realignment, defense technology sharing unprecedented scale, implications for regional balance and alliance structures | Critical |
| **South China Sea Arbitral Tribunal ruling** | July 2016 | Den Haag (The Hague), Nederland (Netherlands) | Definitive international legal adjudication of maritime disputes, China's rejection establishing precedent, implications for rules-based order | Critical |
| **RCEP entry into force** | January 2022 | — | World's largest trade bloc, economic integration milestone, alternative architecture excluding United States | Critical (borderline Critical/High) |
| **Hypothetical major armed clash between regional powers** | — | — | Would represent potential conflict escalation | Critical |
| **Ruaingga (Rohingya) crisis** | August 2017 | Rakhai Pray Nay (Rakhine State), Myanmar | Significant humanitarian crises with massive displacement | Critical |

**Coding Protocols**:
- Consider both immediate incident characteristics and broader strategic context; the same type of incident may receive different significance ratings based on context (e.g., one maritime incident among many = Medium; unprecedented escalation of tactics = High).
- Evaluate significance from a regional perspective rather than global; incidents of critical importance for Southeast Asia receive Critical rating even if global attention is limited.
- When uncertain between adjacent categories, prefer the lower rating (e.g., Medium vs. High ambiguity → code as Medium) to avoid significance inflation, but provide a detailed description supporting a higher rating if warranted.
- Significance assessments may evolve as incidents' longer‑term implications become apparent; initial coding should be based on incident‑time assessment, with potential notes acknowledging subsequent reassessment.
- Use the event description and notes to explain the significance assessment rationale, particularly for High and Critical ratings.

**Evidence Standards**:
- Media coverage intensity and analytical depth (are regional security specialists writing analytical pieces? Are major outlets providing extensive coverage?).
- Official government reactions scope and level (routine statements vs. emergency meetings, working-level vs. leadership responses).
- Policy impact evidence (are governments adjusting strategies, allocating resources, or changing behaviors in response?).
- Expert analysis characterizing incident significance (think tank reports, academic commentary, policy brief assessments).
- Historical comparison (is incident novel or unprecedented? How does it compare to prior similar incidents?).