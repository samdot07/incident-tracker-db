from enum import Enum

# Tables
class ActorType(str, Enum):
    """
    Enumeration of actor types in conflict, security, or governance contexts.
    
    ---
    **Attributes**:
    - `state_military`: Regular armed forces of nation-states.
    - `state_paramilitary`: State-controlled or state-affiliated forces with military capabilities.
    - `government_civilian`: Civilian government agencies and officials.
    - `non_state_armed_group`: Armed organizations operating outside formal state military structures.
    - `criminal_network`: Organized criminal syndicates and networks.
    - `private_security`:  Private military and security companies.
    - `international_organization`: Multilateral intergovernmental organizations.
    - `other`: Residual category for actors not fitting primary classifications.
    """
    state_military = 'State Military'
    state_paramilitary = 'State Paramilitary'
    government_civilian = 'Government Civilian'
    non_state_armed_group = 'Non-State Armed Group'
    criminal_network = 'Criminal Network'
    private_security = 'Private Security'
    international_organization = 'International Organization'
    other = 'Other'
    
class Region(str, Enum):
    """
    Geographic regions used for categorizing locations or data.
    
    ---
    **Attributes**:
    - `mainland_south_eastern_asia`: Cambodia, Lao PDR, Malaysia, Myanmar, Thailand, Viet Nam.
    - `maritime_south_eastern_asia`: Brunei, Indonesia, Philippines, Singapore, Timor-Leste.
    - `eastern_asia`: China, Hong Kong SAR, Macao SAR, DPRK, Japan, Mongolia, ROK.
    - `southern_asia`: Afghanistan, Bangladesh, Bhutan, India, Iran, Maldives, Nepal, Pakistan, Sri Lanka.
    - `central_asia`: Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan.
    - `western_asia`: Armenia, Azerbaijan, Bahrain, Cyprus, Georgia, Iraq, Israel, Jordan, Kuwait, Lebanon, 
            Oman, Qatar, Saudi Arabia, Palestine, Syrian AR, Türkiye, UAE, Yemen.
    
    - `northern_africa`: Algeria, Egypt, Libya, Morocco, Sudan, Tunisia, Western Sahara.
    - `eastern_africa`: BIOT, Burundi, Comoros, Djibouti, Eritrea, Ethiopia, TAAF, Kenya, Madagascar, Malawi, 
            Mauritius, Mayotte, Mozambique, Réunion, Rwanda, Seychelles, Somalia, South Sudan, Uganda, Tanzania UR, Zambia, Zimbabwe.
    - `middle_africa`: Angola, Cameroon, CAR, Chad, Congo, Congo DR, Equatorial Guinea, Gabon, Sao Tome and Principe.
    - `southern_africa`: Botswana, Eswatini, Lesotho, Namibia, South Africa.   
    - `western_africa`: Benin, Burkina Faso, Cabo Verde, Côte d’Ivoire, Gambia, Ghana, Guinea, Guinea-Bissau, 
            Liberia, Mali, Mauritania, Niger, Nigeria, Saint Helena, Senegal, Sierra Leone, Togo.
            
    - `caribbean`: Anguilla, Antigua and Barbuda, Aruba, Bahamas, Barbados, Bonaire, Sint Eustatius and Saba, BVI, 
            Cayman Islands, Cuba, Curaçao, Dominica, Dominican Republic, Grenada, Guadeloupe, Haiti, Jamaica, 
                Martinique, Montserrat, Puerto Rico, Saint Barthélemy, Saint Kitts and Nevis, Saint Lucia, 
            Saint Martin, Saint Vincent and the Grenadines, Sint Maarten, Trinidad and Tobago, 
            Turks and Caicos, USVI.
    - `central_america`: Belize, Costa Rica, El Salvador, Guatemala, Honduras, Mexico, Nicaragua, Panama.
    - `south_america`: Argentina, Bolivia PS, Bouvet, Brazil, Chile, Colombia, Ecuador, Falklands, 
            French Guiana, Guyana, Paraguay, Peru, SGSSI, Suriname, Uruguay, Venezuela BR.
    - `northern_america`: Bermuda, Canada, Greenland, Saint Pierre and Miquelon, US.
    
    - `eastern_europe`: Belarus, Bulgaria, Czechia, Hungary, Poland, Moldova, Romania, Russia, 
            Slovakia, Ukraine.
    - `northern_europe`: Åland, Denmark, Estonia, Faroes, Finland, Guernsey, Iceland, Ireland, Mann,
            Jersey, Latvia, Lithuania, Norway, Svalbard and Jan Mayen, Sweden, UK.       
    - `southern_europe`: Albania, Andorra, Bosnia and Herzegovina, Croatia, Gibraltar, Greece, Holy See, Italy, Malta, Montenegro, 
            North Macedonia, Portugal, San Marino, Serbia, Slovenia, Spain. 
    - `western_europe`: Austria, Belgium, France, Germany, Liechtenstein, Luxembourg, Monaco, Netherlands, Switzerland.
            
    - `australia_and_new_zealand`: Australia, Christmas Island, Cocos (Keeling), HIMI, New Zealand, Norfolk.
    - `melanesia`: Fiji, New Caledonia, Papua New Guinea, Solomons, Vanuatu.
    - `micronesia`: Guam, Kiribati, Marshalls, Micronesia FS, Nauru, CNMI, Palau, USMOI.
    - `polynesia`: American Samoa, Cook Islands, French Polynesia, Niue, Pitcairn, Samoa, Tokelau, Tonga, 
            Tuvalu, Wallis and Futuna.
    
    - `other`: Any region not covered by the above categories.
    """
    mainland_south_eastern_asia = 'Mainland South Eastern Asia'
    maritime_south_eastern_asia = 'Maritime South Eastern Asia'
    eastern_asia = 'Eastern Asia'
    southern_asia = 'Southern Asia'
    central_asia = 'Central Asia'
    western_asia = 'Western Asia'
    
    northern_africa = 'Northern Africa'
    eastern_africa = 'Eastern Africa'
    middle_africa = 'Middle Africa'
    southern_africa = 'Southern Africa'
    western_africa = 'Western Africa'
    
    caribbean = 'Caribbean'
    central_america = 'Central America'
    south_america = 'South America'
    northern_america = 'Northern America'
    
    eastern_europe = 'Eastern Europe'
    northern_europe = 'Northern Europe'
    southern_europe = 'Southern Europe'
    western_europe = 'Western Europe'
    
    australia_and_new_zealand = 'Australia and New Zealand'
    melanesia = 'Melanesia'
    micronesia = 'Micronesia'
    polynesia = 'Polynesia'
    
    other = 'Other'
    
class EventTypeEnum(str, Enum):
    """
    Categorizes events into diplomatic, economic, or military types.
    
    ---
    **Attributes**:
    - **Diplomatic**: 
        - `high_level_summit`: Meetings involving heads of state, heads of government, or equivalent leaders. 
        - `ministerial_engagement`: Activities involving government officials below head of state/government rank.
        - `diplomatic_signaling`: Official government communications, statements, protests, or symbolic actions.
        - `institutional_mechanism`: Establishment, modification, or termination of formal diplomatic institutions, or relations.
    - **Economic**: 
        - `trade_agreement`: Bilateral or multilateral agreements governing trade relations.
        - `investment_and_financing`: Financial initiatives, treaties, agreements, or arrangements.
        - `economic_coercion`: Economic measures employed coercively to influence or punish political behavior.
        - `supply_chain_initiative`: Government-led initiatives addressing supply chain.
    - **Military**: 
        - `maritime_operations`: Naval vessel, coast guard, or maritime militia activities in regional waters.
        - `military_exercises`: Bilateral or multilateral military training exercises.
        - `defense_cooperation`: Defense agreements, treaties, or arrangements enabling foreign military presence.
        - `military_deployment`: Force deployments, stationing, rotational presence, and basing activities.
        - `armed_incident`: Violent military confrontations.
        - `airspace_operations`: Military aircraft operations.
    """
    high_level_summit = 'High Level Summit'
    ministerial_engagement = 'Ministerial Engagement'
    diplomatic_signaling = 'Diplomatic Signaling'
    institutional_mechanism = 'Institutional Mechanism'
    trade_agreement = 'Trade Agreement'
    investment_and_financing = 'Investment and Financing'
    economic_coercion = 'Economic Coercion'
    supply_chain_initiative = 'Supply Chain Initiative'
    maritime_operations = 'Maritime Operations'
    military_exercises = 'Military Exercises'
    defense_cooperation = 'Defense Cooperation'
    military_deployment = 'Military Deployment'
    armed_incident = 'Armed Incident'
    airspace_operations = 'Airspace Operations'
    
class AttributionConfidence(str, Enum):
    """
    Confidence level in attributing an incident to a threat actor.

    ---
    **Attributes**:
    - `confirmed`: Attribution or factual claim supported by official documentation.
    - `suspected`: Attribution or factual claim supported by strong evidence, but retains uncertainty.
    - `third_party`: Attribution made by external credible entity, but not confirmed by evidence.
    - `contested`: Significant disagreement among credible sources.
    """
    confirmed = 'Confirmed'
    suspected = 'Suspected'
    third_party = 'Third Party'
    contested = 'Contested'
    
class StrategicSignificance(str, Enum):
    """
    Strategic importance of an event, asset, or action.

    ---
    **Attributes**:
    - `low`: Incident possesses limited implications.
    - `medium`: Incident possesses notable implications, but does not alter strategic dynamics.
    - `high`: Incident significantly affects relationships, but does not represent crisis-level developments.
    - `critical`: Incident affects regional security.
    """
    low = 'Low'
    medium = 'Medium'
    high = 'High'
    critical = 'Critical'
    
class PoliticalImpact(str, Enum):
    """
    Effect on political relationships or stability.

    ---
    **Attributes**:
    - `improved`: Incident generates measurable improvement in relationships.
    - `stable`: Incident occurs within context of stable relationship without consequences.
    - `deteriorated`: Incident generates measurable worsening of relationships.
    - `ruptured`: Incident generates severe relationship breakdown.
    """
    improved = 'Improved'
    stable = 'Stable'
    deteriorated = 'Deteriorated'
    ruptured = 'Ruptured'
    
class LegalPrecedent(str, Enum):
    """
    Influence on legal interpretation or regulatory frameworks.

    ---
    **Attributes**:
    - `affirming`: Incident demonstrates respect for international law.
    - `neutral`: Incident neither significantly strengthens nor undermines international legal norms.
    - `testing`: Incident probes boundaries of international law.
    - `violating`: Incident constitutes clear violation of international law.
    """
    affirming = 'Affirming'
    neutral = 'Neutral'
    testing = 'Testing'
    violating = 'Violating'
     
class LocationType(str, Enum):
    """
    Categorizes geographic locations for geopolitical and administrative contexts.

    ---
    **Attributes**:
    - `disputed_island`: A landmass with unresolved sovereignty claims.
    - `maritime_feature`: Oceans, seas, or other significant water bodies.
    - `border_region`: Areas straddling or adjacent to international boundaries.
    - `capital_city`: The official seat of government.
    - `military_installation`: Bases, forts, or strategic defense locations.
    - `economic_zone`: Exclusive economic zones (EEZ) or other resource‑control areas.
    - `international_waters`: Areas beyond any national jurisdiction.
    - `other`: Fallback for locations not covered by the above categories.
    """
    disputed_island = 'Disputed Island'
    maritime_feature = 'Maritime Feature'
    border_region = 'Border Region'
    capital_city = 'Capital City'
    military_installation = 'Military Installation'
    economic_zone = 'Economic Zone'
    international_waters = 'International Waters'
    other = 'Other'
    
class SourceType(str, Enum):
    """
    Represents the type of source for a data record.

    ---
    **Attributes**:
    - `academic_dataset`: Data from academic research or institutional repositories.
    - `government_release`: Official data published by a government agency.
    - `think_tank_report`: Reports produced by policy or research organizations.
    - `news_article`: Current or historical news coverage.
    - `primary_document`: Original, uninterpreted records or documents.
    - `book`: Published books, including monographs and edited volumes.
    - `academic_journal`: Peer-reviewed journal articles.
    - `other`: Any source type not covered by the other categories.
    """
    academic_dataset = 'Academic Dataset'
    government_release = 'Government Release'
    think_tank_report = 'Think Tank Report'
    news_article = 'News Article'
    primary_document = 'Primary Document'
    book = 'Book'
    academic_journal = 'Academic Journal'
    other = 'Other'

# Junction tables
class InvolvementType(str, Enum):
    """
    Represents the type of involvement a country can have in a case or narrative.

    ---
    **Attributes**:
    - `primary_actor`: The main party driving the events.
    - `supporting_actor`: A secondary party assisting or influencing the primary actor.
    - `affected_party`: Someone impacted by the events but not directly involved in driving them.
    - `mediator`: A neutral party facilitating resolution or communication.
    - `observer`: A party present or monitoring without direct participation.
    """
    primary_actor = 'Primary Actor'
    supporting_actor = 'Supporting Actor'
    affected_party = 'Affected Party'
    mediator = 'Mediator'
    observer = 'Observer'
    
class ActorRole(str, Enum):
    """
    Enumeration of possible roles an actor can assume in a system interaction.

    ---
    **Attributes**:
    - `initiator`: The actor who starts or initiates the action.
    - `responder`: The actor who responds to the initiator.
    - `target`: The actor who is the focus or recipient of the action.
    - `participant`: An actor who takes part but does not hold a primary role.
    - `claimant`: The actor who asserts a claim or right in the context.
    - `observer`: An actor who watches or monitors without direct involvement.
    """
    initiator = 'Initiator'
    responder = 'Responder'
    target = 'Target'
    participant = 'Participant'
    claimant = 'Claimant'
    observer = 'Observer'