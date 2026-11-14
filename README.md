# Astrocyte — team template

A runnable Streamlit project with an original interactive seven-zone Mars outpost map. The habitat pages contain only their titles, ready for your team to build on. The purple branding, crew sidebar and existing crew pages are preserved. The map shows a concept habitat, not live systems telemetry.

## Run on your current Mac

```bash
cd /Users/aris/nasa_hackathon/Astrocyte
.venv/bin/python -m streamlit run app.py
```

Open the Local URL printed in the terminal, normally http://localhost:8501. Keep the terminal running; Ctrl+C stops the website. Use the Streamlit command above instead of VS Code's Run Python File button.

## Fresh setup — macOS / Linux

Install Python 3.12 and Git, then run:

```bash
git clone https://github.com/jstitckd/Astrocyte.git
cd Astrocyte
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `python3 --version` already reports Python 3.12, `python3 -m venv .venv` also works. Run commands from the folder containing `app.py` and `requirements.txt`. The shared GitHub repository must include this template change before your partners can clone it.

## Fresh setup — Windows PowerShell

```powershell
git clone https://github.com/jstitckd/Astrocyte.git
cd Astrocyte
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If activation is blocked, use the interpreter directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Each developer creates one `.venv` inside their clone. Do not commit or share it. The separate environment in the parent `nasa_hackathon` folder is not used by this project.

## VS Code

Open `Astrocyte.code-workspace`, install Microsoft's Python extension, and run **Python: Select Interpreter** from the Command Palette. Select this project's `.venv/bin/python` on Mac or `.venv\Scripts\python.exe` on Windows. Terminal activation and VS Code's selected interpreter are separate; selecting one does not necessarily update the other.

The workspace also provides **Run and Debug → Run Astrocyte** (requires the Python Debugger extension).

## Where to add your content

| Habitat space | Page file |
| --- | --- |
| Base overview / interactive map | `views/home.py` |
| Main living & working quarters | `views/living.py` |
| Environmental control & life support | `views/life_support.py` |
| Science laboratories & maintenance workshops | `views/science.py` |
| Exercise quarters | `views/exercise.py` |
| Power generation & storage | `views/power.py` |
| Greenhouse | `views/greenhouse.py` |
| Spaceship & launch area | `views/launch.py` |
| Data & exports | `views/data.py` |

The map's labelled space guide provides the same routes as the drawing. Hover/focus shows the area's description and facilities; clicking a building or guide entry opens its page. On mobile, a guide tap previews the area, then **Open space** navigates. Direct building taps also work.

Existing crew routes (including `views/Alex.py`) and older health page files remain available; the new map does not overwrite them.

Every page has a small `render()` function. Add your Streamlit code below its title, inside that function. The homepage already calls `render_base_map()` and handles its selected destination. There is no common dashboard file to edit; each page can be developed independently.

```python
# Example to add inside a page's render() function:
st.write("Your content goes here.")
```

The seven destination pages intentionally contain no sample widgets or placeholder instructions on screen.

## Other folders

| File / folder | Purpose |
| --- | --- |
| `app.py` | Loads the styling and connects page IDs to their `render()` functions. |
| `components/sidebar.py` | Shared logo and working navigation. Put future reusable widgets under `components/`. |
| `models/areas.py` | `HABITAT_AREAS`: seven map destinations, labels, descriptions and facilities. Original `AREAS` remains for older pages. |
| `models/metrics.py` | Empty metric dictionary for the team to define later. |
| `frontend/styles.css` | Minimal styling for the shared shell. |
| `frontend/map/` | Editable map drawing (`index.html`), colours (`map.css`) and interactions (`map.js`). |
| `components/base_map.py` | Embeds the map and validates building selections. |
| `services/` | Empty workspace for your own data, validation and storage modules. |
| `data/` | Empty dataset workspace; no synthetic data is loaded. |
| `tests/test_app.py` | Checks navigation, blank destination pages, map routes and event handling. |
| `docs/` | Current architecture, interfaces and verification notes. |
| `.streamlit/config.toml` | Streamlit theme and settings. |
| `requirements.txt` | Python runtime dependencies. |

Only Streamlit is used by the template. The existing pandas, Plotly and NumPy dependencies remain available for your team to use when adding features.

## Suggested four-person split

- **Person 1:** `frontend/` and `views/home.py` — illustration, styling and map interactions.
- **Person 2:** `views/life_support.py`, `power.py`, `data.py` and shared data services — coordinate contracts with page owners.
- **Person 3:** `views/living.py`, `exercise.py` and `greenhouse.py` — crew habitat pages.
- **Person 4:** `views/science.py`, `launch.py`, existing crew pages and shared integration in `app.py` and `models/areas.py`.

Coordinate changes to shared files before editing. See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch workflow and [docs/interfaces.md](docs/interfaces.md) for the small shared contract.

## Checks

```bash
python -m unittest discover -s tests -v
```

The six integration tests check habitat and legacy routes, the crew sidebar, blank habitat pages, map-message validation, return navigation and matching Python/SVG IDs. Real-browser checks cover all seven regions and guide links, hover descriptions, keyboard and mobile interactions; see `docs/verification.md`.

## What is deliberately absent

The habitat map adds no measurements, forms, checklists, storage, API connection or database. The team's existing crew page remains separate. The **Data & exports** destination is a blank page name, not an implemented feature. Add these pieces as your team designs them.

The previous full prototype remains recoverable from Git history (commit `aef6f9d`). The previously generated `docs/code-layout-guide.html` is preserved as a historical guide to that prototype; it does not describe this simplified layout. Use the current README and architecture notes for the skeleton.

To customise the homepage map, begin with [frontend/map/README.md](frontend/map/README.md). Change colour variables in `map.css`, building positions and shapes in `index.html`, and interaction behaviour in `map.js`.

The project keeps the Streamlit Community Cloud entry point `app.py`. Deployment instructions and team workflows are in the documentation; this local template change has not been pushed or deployed automatically.

## Troubleshooting

- **Missing `requirements.txt`:** `cd` into the `Astrocyte` repository folder first.
- **`ModuleNotFoundError`:** select/activate this project's `.venv`, then install with `python -m pip install -r requirements.txt`.
- **Underlined Streamlit import:** explicitly choose the `.venv` interpreter in VS Code.
- **Cannot connect in the browser:** restart `python -m streamlit run app.py` and open the exact printed URL.
- **Port already in use:** stop the old process with Ctrl+C or add `--server.port 8502` and use its printed URL.
