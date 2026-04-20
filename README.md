# Image-based urban analysis

Prototype for the 2026 Arch_Manu hackathon: combine streetscape-style vision exports with web and census context, then synthesise narrative and structured “urban DNA” via the OpenAI API.

## What’s in the repo


| Path                      | Role                                                                                                             |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `analysis.py`             | Main script: loads vision data, runs pattern, insights, and place agents, then calls the synthesis agent.        |
| `agents.py`               | Agent functions using `OpenAI` (`client.responses.create`).                                                      |
| `vision_example.json`     | Example streetscape analyser export from clause used as stand-in vision input for the vision agent (see below)`. |
| `lib/metadata_extract.py` | Optional utility: EXIF subset and per-image pixel statistics for files under `images/`.                          |
| `images/`                 | Sample photos for `metadata_extract` when run as a script.                                                       |


## Agents (`agents.py`)

- **Pattern agent** — Finds cross-image patterns from the supplied JSON (creative / non-obvious angles).
- **Insights agent** — Urban analyst lens: CPTED, accessibility, lighting, noise, etc.
- **Place agent** — Fetches place based information from a supplied address from google maps and realestate URLs. Also scrapes ABS census quickstats page, then asks the model to summarise insights for contextual, place based information.
- **Synthesis agent** — Merges vision, place, pattern, and insights into a narrative plus an “URBAN DNA” style summary.

**Not fully wired for the main pipeline**

- `**vision_agent`** — Placeholder. To be replaced with dedicated LVM eg openfacades. Currently  vision.example is used as a sythetic output for the function.
- `**context_agent**` — Placeholder. Will be used to extract google reviews to understand the vibe/community feeling of the place.

## Workflow

- **execute `analysis.py`.**
- Script executes agents in this order 
- vision agent ---> Pattern Agent ---> Insights Agent ---> Place Agent 
- Each agent outputs a string of text or a JSON
- Sythesis agent merges vision, place, pattern, and insights into a narrative plus an “URBAN DNA” style summary

## Prerequisites

- Python 3.x
- An OpenAI API key available to the SDK (typically a `.env` file with `OPENAI_API_KEY=...`; see [OpenAI Python library](https://github.com/openai/openai-python) for env var names your version expects).

Dependencies used in code (install as needed, e.g. with `pip`):

- `openai`
- `python-dotenv`
- `requests`
- `beautifulsoup4`
- `Pillow`

## Configuration

- **API key:** use `.env` (ignored by git per `.gitignore`) so keys are not committed.
- **Place agent:** address, listing URLs, and census URL are currently hard-coded in `place_agent()` inside `agents.py`; adjust there for other sites.

## Sample Output

### NARRATIVE SUMMARY

**Vision**


Macquarie Street in Parramatta is envisioned as a balanced CBD street that preserves the legibility of a high-rise office spine while delivering continuous ground-floor vitality. The plan emphasizes activated frontages, greenery, and shade to transform the footpath into a welcoming social space, day and night. Ground-floor uses such as retail, cafes, and community facilities would weave human-scale activity into the street, supported by universal access, better lighting, and CPTED-informed design. The street would retain its architectural drama — tall towers and bold massing — but pair that with inviting, permeable edges and programming that encourages lingering, exchange, and civic life.

**Place**


This segment of Parramatta’s CBD sits at a crossroads of transit, commerce, and services, with strong pedestrian and vehicular infrastructure. Wide brick-paved footpaths and canopy coverage delineate a clear street wall, yet activation is episodic, dominated by corporate podiums and a limited set of ground-floor uses. Demographics show a young, diverse population with substantial rental housing, reflecting Parramatta’s growth trajectory as a regional hub. The street benefits from proximity to Parramatta Station and Church Street amenities, but the current character feels utilitarian. Opportunities lie in continuous activation, integrated greenery, and seating to humanize the public realm.       

**Pattern**


Across the dataset, a clear pattern emerges: strong vertical enclosure and wide footpaths coexist with low street-level activation. Architectural drama (glass façades, tower bases, and sculptural columns) does not translate into vibrant street life. Green infrastructure is scarce, relying on building overhangs rather than trees or permeable planting. Ground-floor activation is episodic, with pockets of engagement around certain storefronts (e.g., Ray White, NAB) but no continuous active edge. CPTED opportunities are present but require more consistent lighting, permeability, and programming to convert movement into sociable dwell time.

**Insights**


The streetscape exhibits a paradox of impressive enclosure and modest sociability. Walkability is decent, but pedestrian activity remains sparse without active uses and greenery. Activation strategies should couple ground-floor retail and hospitality with contextual design cues, while introducing street trees, seating, and permeable edges to foster surveillance and comfort. Accessibility and inclusivity must be embedded in every frontage. Elevating the street with programmed events, small plazas, and human-scale interventions can transform this corridor into a safe, inviting, and economically viable urban spine for Parramatta.

### URBAN DNA

{  "**Height Range**": "Mid-to-high-rise skyline dominated by office towers; precise heights not specified",  
"**Dominant Use**": "Commercial/office",  
"**Primary Typology**": "Office towers with active ground-floor edges; CBD street with podiums and large-scale enclosure",  
"**Material Palette**": "Glass curtain walls, brick-paved footpaths, concrete/grey cladding, metal canopies, planters and limited greenery",  
"**Activity Level**": "Moderate walkability with low daytime pedestrian activation; room for improved sociability and lingering activity",  
"**Style**": "Contemporary corporate / modernist with prominent vertical massing and sculptural features (e.g., V-shaped columns)",  
"**Confidence**": 0.8,

  "**Demographics**": 
  {    "*Population*": 493515,  
  "*MedianAge*": 34,  
  "*IndigenousPct*": 0.8,  
  "*LanguagesAtHome*": { "EnglishOnly": 32.4,   "NonEnglish": 67.3,   "TopLanguages": ["Arabic 10.0%", "Mandarin 8.3%", "Cantonese 4.7%", "Korean 3.4%", "Nepali 2.9%"]  },  
  "*MedianWeeklyIncome*": 1828,  
  "*UnemploymentRate*": 7.0,  
  "*Housing*": {      "OwnedOutright": 22.2,"OwnedWithMortgage": 29.7,"Rented": 44.6,"AvgPeoplePerDwelling": 2.8,"DwellingTypes": "Separate house 46.6%, Flat/apartment 38.6%, Semi-detached 14.2%"    },  
  "*Occupations*": "Professionals 28.7%, Clerical/Administrative 14.2%, Managers 11.8%, Technicians/Trades 10.3%, Community and Personal Service 9.4%", 
  "*Industries*": "Computer System Design 4.4%, Hospitals 4.4%, Banking 3.1%, Supermarkets 2.9%, Aged Care Residential Services 2.5%",  
  "*HouseholdComposition*": "Family households 73.1%, One person 21.6%, Group 5.3%"       },

"**Insights**": "Parramatta’s urban core is growing as a regional hub with a young, diverse workforce and high renter occupancy. The area benefits from strong transport access and a dense retail spine, yet streetscapes lean toward efficiency over activation. Data-driven opportunities point to ground-floor retail activation, strategic greenery, and programmable spaces that could unlock daytime and nighttime liveliness, while preserving the legibility of a high-rise corporate district."}