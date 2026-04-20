# Image-based urban analysis

Prototype for the 2026 Arch_Manu hackathon: combine streetscape-style vision exports with web and census context, then synthesise narrative and structured “urban DNA” via the OpenAI API.

## What’s in the repo

| Path | Role |
|------|------|
| `analysis.py` | Main script: loads vision data, runs pattern, insights, and place agents, then calls the synthesis agent. |
| `agents.py` | Agent functions using `OpenAI` (`client.responses.create`). |
| `vision_example.json` | Example streetscape analyser export from clause used as stand-in vision input for the vision agent (see below)`. |
| `lib/metadata_extract.py` | Optional utility: EXIF subset and per-image pixel statistics for files under `images/`. |
| `images/` | Sample photos for `metadata_extract` when run as a script. |

## Agents (`agents.py`)

- **Pattern agent** — Finds cross-image patterns from the supplied JSON (creative / non-obvious angles).
- **Insights agent** — Urban analyst lens: CPTED, accessibility, lighting, noise, etc.
- **Place agent** — Fetches place based information from a supplied address from google maps and realestate URLs. Also scrapes ABS census quickstats page, then asks the model to summarise insights for contextual, place based information.
- **Synthesis agent** — Merges vision, place, pattern, and insights into a narrative plus an “URBAN DNA” style summary.

**Not fully wired for the main pipeline**
- **`vision_agent`** — Placeholder. To be replaced with dedicated LVM eg openfacades. Currently  vision.example is used as a sythetic output for the function.
- **`context_agent`** — Placeholder. Will be used to extract google reviews to understand the vibe/community feeling of the place.

## Workflow

* **execute `analysis.py`.**
* Script executes agents in this order 
* vision agent ---> Pattern Agent ---> Insights Agent ---> Place Agent 
* Each agent outputs a string of text or a JSON
* Sythesis agent merges vision, place, pattern, and insights into a narrative plus an “URBAN DNA” style summary




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
