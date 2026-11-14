# Project map and team boundaries

The entry point only assembles navigation and views. Data and storage modules import no Streamlit code, so Person 2 can develop and test them without the website running. There is no `pages/` directory: Streamlit's automatic pages would compete with the explicit sidebar/map navigation.

| Path | Purpose | Owner |
| --- | --- | --- |
| `app.py` | Page configuration, sidebar context, view dispatch, shared data indicator and footer. | Person 3 integrates |
| `models/metrics.py` | Accepted metric IDs, units, meanings, daily-total list, crew display names and six-column schema. | Person 2 |
| `models/areas.py` | Area IDs, names, dashboard metrics, form types and default tasks. | Person 3 integrates with owners |
| `services/ingestion.py` | CSV parsing, all-or-nothing validation, inclusive UTC filtering and CSV serialization. | Person 2 |
| `services/demo.py` | Seeded synthetic readings with explicit synthetic sources. | Person 2 |
| `services/storage.py` | Session-scoped imports, validated check-ins, completion, custom EVA lists and JSON export. | Person 2 |
| `services/adapters.py` | Protocol and validation boundary for a future provider. No provider is connected. | Person 2 |
| `services/navigation.py` | Validate/deduplicate map messages and resolve area IDs. | Person 1 with Person 3 |
| `components/context.py` | Small dataclass passed to views; defines the current filters and storage handle. | Shared contract |
| `components/sidebar.py` | Source/import controls, crew/date filters and accessible route buttons. | Person 3 integrates with Person 2 |
| `components/base_map.py` | Local Streamlit component; passes the registry into the HTML map. | Person 1 |
| `components/readings.py` | Latest-reading cards and Plotly history with source/UTC labels. | Person 3 |
| `components/forms.py` | Area-specific self-report forms and history. | Person 3 |
| `components/tasks.py` | Scoped task checkboxes, progress count and configurable EVA checklist. | Person 3 |
| `views/home.py` | Homepage composition, map event handling and summary. | Person 1 |
| `views/dashboard.py` | Common dashboard layout; dispatches the area's metrics, tasks and form. | Person 3 |
| `views/data.py` | Sample download, schema table, measurement/workflow exports and storage explanation. | Person 3 with Person 2 |
| `frontend/map/` | Original SVG buildings (`index.html`), accessible interactions/bridge (`map.js`), map styles (`map.css`). No build step or CDN. | Person 1 |
| `frontend/styles.css` | Shared dark dashboard styling and responsive rules. | Person 1 |
| `data/sample_readings.csv` | Safe synthetic sample that round-trips through the importer. | Person 2 |
| `tests/` | Data/store unit tests, Streamlit AppTest integration tests, optional browser smoke script. | Each owner tests their work |
| `docs/` | Shared interfaces, data contract, architecture and verification notes. | All three |
| `.streamlit/config.toml` | Safe shared theme, 5 MB upload limit and telemetry preference. | Person 1 |
| `requirements.txt` | Pinned direct runtime dependencies. | Coordinate changes |
| `Astrocyte.code-workspace` | Portable project `.venv` selection and Streamlit debugger launch. | Shared |
| `.python-version` | Recommended Python 3.12 for local toolchains. | Shared |
| `.gitignore` | Keeps environments, personal settings, caches, secrets and local runtime data out of Git. | Shared |

`__init__.py` files mark Python packages and contain no application logic. `README.md` is the first-run guide; `CONTRIBUTING.md` is the Git workflow.

## How state moves

The sidebar selects a demo or validated imported DataFrame. `filter_readings()` selects the crew and inclusive UTC window. A `ViewContext` carries that result and `SessionStore` to the active view. The map and sidebar share area IDs from the registry.

Forms save separate records with an observation date, creation timestamp and dataset ID. Task keys include dataset, crew, observation date, area and task ID. Check-ins never modify readings. Custom EVA lists are per crew member within the session; their stable content-based task IDs preserve completion when an unchanged item is reordered.

Imported snapshots live in session state, not in Streamlit's cross-user cache. Only the deterministic synthetic dataset is cached. Normal reruns preserve session records; disconnect/restart/refresh may lose them. There are no local runtime files and no SQLite database in this prototype.

## Extensions

Start with the function examples in [interfaces.md](interfaces.md). Add metrics in the metric registry and generator, then assign them to an area. Add tasks in the area registry. A new building needs an area entry and a labelled SVG region with the same `data-area` ID; navigation and the generic chart layout follow the registry. A truly new form type also needs fields/validation in `components/forms.py` and `services/storage.py`.

When introducing durable storage, change the storage implementation and tests behind the same interface. Decide user identity, authorization and ownership before sharing health data between users. Do not silently switch the current isolated session store to a global file.
