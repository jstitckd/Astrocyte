# ✳ Astrocyte

A working Mars-habitat crew health prototype built for three students who mainly know Python. Python + Streamlit + Plotly, with an original SVG/JavaScript habitat map. Free to run locally; no API account, paid assets, Node build or credentials required.

The homepage is a map of six connected spaces. Hover or keyboard-focus a building to preview its tasks; click or press Enter/Space to open the dashboard. On a phone, tap a building and then **Open dashboard**. Every destination is also available in the sidebar.

| Space | What you can do |
| --- | --- |
| Sleeping quarters | Review resting heart rate, HRV and sleep duration; write a recovery observation. |
| Exercise area | Review activity duration and exercise heart rate; save exercise duration and notes. |
| Medical bay | Review available vital signs; save symptoms and observations. |
| Kitchen | Review daily fluid and energy totals; log meals, drinks and entry amounts separately. |
| Greenhouse / common room | Save mood and stress self-ratings; review past entries and a history graph. |
| Airlock / EVA | Review EVA duration and recorded exposure; edit and complete a pre-EVA checklist and save notes. |

All demo readings are synthetic: 3 crew members, 14 days (1–14 November 2026), 462 readings. There are no live sensors, diagnoses, invented health scores or automated clinical alerts. The map is an original schematic, not a navigational plan. Use synthetic data for a public demo.

## Start here on your current Mac

The rebuilt project and its only project environment are here:

```bash
cd /Users/aris/nasa_hackathon/Astrocyte
.venv/bin/python -m streamlit run app.py
```

Open the URL printed in the terminal, normally http://localhost:8501. Keep the terminal open. **Ctrl+C stops the server.** Run the command again to restart. Do not use VS Code's **Run Python File** button: Streamlit needs its own launcher.

The separate `.venv` in the parent `nasa_hackathon` folder is not used. Do not copy, share or commit a virtual environment; each developer creates one inside their own `Astrocyte` clone.

## Fresh setup: macOS / Linux

Install Python **3.12** and Git. Clone once into your chosen projects folder:

```bash
git clone https://github.com/jstitckd/Astrocyte.git
cd Astrocyte
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `python3.12` is unavailable, install Python 3.12 first. `python3 --version` may already report 3.12; in that case use `python3 -m venv .venv`. Every command after `cd Astrocyte` runs from the folder containing `app.py` and `requirements.txt`.

For later sessions:

```bash
cd /path/to/your/Astrocyte
source .venv/bin/activate
python -m streamlit run app.py
```

If the repository is already cloned, run `git pull --ff-only` in it instead of cloning again. The GitHub copy must include this rebuild before partners can download it.

## Fresh setup: Windows PowerShell

Install Python **3.12** and Git, then:

```powershell
git clone https://github.com/jstitckd/Astrocyte.git
cd Astrocyte
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, no policy change is required. Use the environment's interpreter directly, from the `Astrocyte` folder:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## VS Code: select the project interpreter

1. Install the Microsoft **Python** extension. Install **Python Debugger** if you want F5 debugging.
2. Choose **File → Open Workspace from File** and open `Astrocyte.code-workspace`. It opens the correct project root and defaults to its `.venv` folder on either operating system.
3. Press **Cmd+Shift+P** (Mac) or **Ctrl+Shift+P** (Windows), run **Python: Select Interpreter**, and choose the environment inside this project.
   - Mac: `/Users/aris/nasa_hackathon/Astrocyte/.venv/bin/python` on this machine.
   - Windows: `<your clone>\.venv\Scripts\python.exe`.
4. Open a new terminal and use `python -m streamlit run app.py`, or select **Run and Debug → Run Astrocyte**.

Terminal activation changes that terminal's `PATH`. VS Code's language server and debugger keep their own interpreter selection, which can be cached. Activating a terminal environment therefore may not remove an import underline: explicitly select the interpreter above, and use **Developer: Reload Window** if needed. `python -c "import sys; print(sys.executable)"` shows which interpreter your terminal is using.

## Try the full workflow

1. Start with **Demo mission** in the sidebar. Choose a crew member and UTC date window.
2. Explore a building. The latest cards and Plotly graphs show measurements for those filters, with timestamps, units and sources. Hover the graph for details; drag to zoom and double-click to reset.
3. Choose the **Check-in & checklist date** within that window. Save an observation or use the area's form, then mark a checklist item complete. This date scopes the entry and tasks; charts retain the whole date window.
4. In the greenhouse, set mood/stress ratings and save. The history and graph reflect your own entries, not a medical score.
5. In the airlock, expand **Edit pre-EVA checklist**. Enter 1–12 items, one per line, and save. The configuration belongs to the selected crew member in this session. It is illustrative and does not replace mission procedures.
6. Open **Data & exports**, download the sample, select **Imported CSV** in the sidebar, and upload it. The indicator changes from **SIMULATED DATA** to **IMPORTED CSV**. A valid upload replaces readings; a failed upload leaves the last valid import loaded and shows the reason.
7. Export filtered readings as CSV, and check-ins/tasks/custom EVA lists as JSON. The JSON includes all crew and datasets in this browser session; it is an archive, not a restore format. Imported values and self-reported entries never overwrite each other.

Empty windows show dashes and an explanation rather than a fabricated value. Initial loading uses Streamlit's running indicator; CSV validation shows a spinner. Data is a static snapshot and never automatically refreshes from a device.

## Where each teammate starts

Read [the shared interfaces](docs/interfaces.md) together before changing signatures or IDs. The contracts were defined first so the three workstreams can stay independent.

| Owner | Start here | Responsibility |
| --- | --- | --- |
| Person 1 | `frontend/map/index.html`, `map.css`, `map.js`; `frontend/styles.css`; `views/home.py` | Illustration, hover/focus/tap interactions, homepage and visual styling. |
| Person 2 | `models/metrics.py`; `services/`; `data/`; `tests/test_data.py`, `test_storage.py` | Data contract, CSV validation, session storage and future provider adapters. |
| Person 3 | `views/dashboard.py`; `views/data.py`; `components/forms.py`, `readings.py`, `tasks.py`; `tests/test_app.py` | Charts, forms, dashboards and task workflows. Integrates small changes to `app.py` and `models/areas.py`. |

See [CONTRIBUTING.md](CONTRIBUTING.md) for branches, pull requests and conflict resolution, and [architecture](docs/architecture.md) for every module's purpose and extension steps.

## Data flow and persistence

```text
Synthetic generator / uploaded CSV / future provider
                         ↓
          services/ingestion.py validates all rows
                         ↓
            SessionStore holds imported readings
                         ↓
          crew + inclusive UTC date-range filter
                         ↓
                 cards, charts, CSV export

Forms → validate → separate session check-in records → history / JSON export
Tasks → dataset + crew + date + area completion → progress / JSON export
```

Accepted columns: `timestamp,crew_id,metric,value,unit,data_source`. See [data-contract.md](docs/data-contract.md) for exact metrics, units, timestamp interpretation, daily-total semantics and adapter examples.

**Storage is browser-session memory only.** Normal widget interactions and navigation preserve it. Refreshes, new tabs, disconnects and restarts can start a new session and lose imports, check-ins, tasks and custom lists. Nothing is written to local runtime files, shared with other crew, or persisted to a database. Export before disconnecting. Identical CSV bytes reuse a dataset scope; different bytes create a new task/check-in scope.

## Checks

From the repository root with `.venv` activated:

```bash
python -m unittest discover -s tests -v
python -m pip check
```

Tests cover invalid files, UTC conversion, inclusive filtering, CSV round trips, adapter boundaries, scoped storage, failed imports, all six navigation destinations, every form, task progress and export controls. Streamlit may print `missing ScriptRunContext` during AppTest setup; passing tests do not need a running server.

Optional real-browser checks are in [docs/verification.md](docs/verification.md), including results and any verification limits. They are separate from the app's runtime dependencies.

## Deploy on Streamlit Community Cloud

1. Commit and push this source to the shared GitHub repository. Track all source, `requirements.txt`, `.streamlit/config.toml`, the frontend files and synthetic CSV. Do not upload `.venv`, secrets or personal data.
2. Sign in at https://share.streamlit.io and choose **Create app**. Select the repository and branch containing this code, and set the main file path to **`app.py`**.
3. Open **Advanced settings**, select **Python 3.12**, then deploy. Community Cloud installs `requirements.txt`; no Node or OS packages are needed.
4. If you later add a provider, set its secrets in the hosting settings. Locally use `.streamlit/secrets.toml` or environment variables; both local secrets files and `.env` are ignored by Git.

This is deployment-ready source, not an already deployed service. Session state on Community Cloud has the same limitations as local use. There is no durable storage, shared crew database, authentication or production access control. A future SQLite file would also be local to the server and can be lost on redeploy; use an appropriate external persistent store if that becomes a requirement.

Deployment steps follow Streamlit's [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [dependency guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `requirements.txt` not found | Your terminal is in the wrong folder. `cd` into the cloned `Astrocyte` folder; `ls` on Mac or `dir` on Windows should show both `app.py` and `requirements.txt`. |
| `ModuleNotFoundError: streamlit` (or pandas/plotly) | Activate this project's `.venv`, then run `python -m pip install -r requirements.txt`. Use `python -m pip`, so installation matches the interpreter you run. |
| Streamlit import is underlined but the site runs | Select the `.venv` interpreter explicitly in VS Code; terminal activation and the editor selection are separate. |
| A Python file runs but no website appears | Use `python -m streamlit run app.py`, not `python app.py` or Run Python File. |
| Browser says it cannot connect | The server stopped or you used the wrong port. Restart the command and open the exact Local URL printed in that terminal. Keep it running. |
| Port 8501 is already in use | Stop the old app with Ctrl+C, or run `python -m streamlit run app.py --server.port 8502`. Open the printed URL. |
| My partner sees the old or empty project | Commit and push your changes; they should `git pull --ff-only`, then reinstall `requirements.txt`. Their `.venv` is private to their machine. |
| `python3.12` / `py -3.12` not found | Install Python 3.12 and reopen the terminal. Check the version before creating `.venv`. |
| CSV is rejected | Read the error next to the uploader. Use the sample format, exact metric IDs/units and ISO timestamps; daily totals cannot have multiple rows per crew/date/metric. |
| Tasks or check-ins disappeared | Check the crew, date and dataset filters. A refresh/disconnect/restart may also have ended the session. This prototype has no restore function. |

## Current scope

No wearable/API connection, automated medical judgement, clinical alerts, durable database, login or multi-user synchronization. CSV exports are measurements, while JSON exports are session workflows. Forms are observations for review, not a diagnostic tool. The SVG is an original Mars-base illustration; no reference image file was included with the text brief.
