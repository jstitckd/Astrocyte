# Astrocyte — Mars habitat health dashboard

A complete runnable Streamlit prototype with an original isometric SVG Mars-base map. Hover or keyboard-focus a building to see its tasks; click or press Enter to open the corresponding dashboard. Touch users can tap a building. No Node build, paid API, or image service is needed.

## Start on macOS / Linux

Install Python 3.12 or 3.13. Unzip this project, then open the `astrocyte` folder in VS Code. In VS Code's terminal (Terminal → New Terminal):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the Local URL printed in the terminal, usually http://localhost:8501. Keep the terminal running. Stop with Control+C. On later launches, activate the environment and run the last command again. In VS Code, choose `.venv/bin/python` using Python: Select Interpreter.

Windows: create the environment with `py -m venv .venv`, then activate with `.venv\Scripts\Activate.ps1` in PowerShell; the remaining `python` commands are the same.

## Included

- Interactive original Mars-base diagram: sleeping quarters, medical bay, exercise area, kitchen, greenhouse, and airlock.
- Six functioning dashboards with metric cards and selectable Plotly history graphs.
- Three simulated crew members and 504 example readings across 14 days.
- Crew and date filters; UTC timestamps and last-record dates.
- Per-crew, per-source, daily task checklists and session progress.
- Health / exercise / nutrition / EVA notes and mood/stress check-ins.
- CSV upload with size, schema, units, timestamp, numeric and duplicate validation.
- JSON exports of loaded readings and session check-ins/tasks, plus a sample CSV download.
- Sidebar fallback navigation; responsive map; keyboard-accessible regions.

## Files

- `app.py`: Streamlit layout, navigation, charts, CSV input, session check-ins and tasks.
- `frontend/index.html`: original SVG map, hover panel, keyboard/click handlers, and Streamlit component message bridge. No external CDN dependencies.
- `data_model.py`: accepted metrics, units, validation and deterministic sample data.
- `data/sample_health_data.csv`: ready-to-upload sample readings.
- `.streamlit/config.toml`: dashboard theme.
- `requirements.txt`: versions used during checks.
- `test_app.py`: automated Python validation and app-flow tests.

## External data

In the sidebar, select **Upload CSV** and upload `data/sample_health_data.csv` to try importing. The file replaces the displayed dataset; it does not append to previous uploads.

Required columns:

```csv
timestamp,crew,metric,value,unit
2026-11-14T08:00:00Z,Alex Morgan,heart_rate,64,bpm
```

See **Data & exports** for all accepted metric identifiers and exact units. Use ISO 8601 timestamps with offsets; naive timestamps are treated as UTC. Daily intake/activity/exposure values represent daily totals, not incremental events. Duplicate crew/timestamp/metric keys are rejected. Metric cards show the latest value in the selected range; no baseline comparisons or diagnoses are inferred.

There is no live wearable/API connector in this prototype because no provider or credentials have been selected. To add one, write a Python adapter that fetches data, converts it to the five columns, and calls `validate_frame(df)` before displaying it. Keep tokens in `.streamlit/secrets.toml` locally or the hosting service's secrets settings. Never commit secrets to GitHub.

## Session storage and scope

Task completion and check-ins live in Streamlit session state only. They are not shared across users and may reset when the session disconnects or the app restarts. Export JSON before closing. Imported data is not stored in a database. Session exports contain all crew members' notes entered in that session. Self-reported check-ins do not overwrite sensor history.

This is a hackathon prototype, not a clinically validated medical device. The SVG is an original schematic inspired by the requested isometric layout, not a reproduction of the attached image. Demo readings are clearly marked synthetic. EVA task labels are illustrative and do not replace mission procedures. No login, durable database, real sensors, automated medical advice, or production access controls are included. Use synthetic/de-identified data for public demonstrations.

## GitHub and deployment

Copy the project contents into your team's repository. Keep the `frontend` directory beside `app.py`, including `index.html`. Commit the sample data, `.streamlit/config.toml`, requirements and source. Do not commit `.venv` or `.streamlit/secrets.toml` (the included `.gitignore` excludes them).

In Streamlit Community Cloud, create an app from that GitHub repository, choose the branch and `app.py` entry point, and select Python 3.12. If you keep the project in a subfolder, set the entry point to `astrocyte/app.py`. The code is ready for Streamlit hosting but has not been deployed to your account.

Suggested team split: map/design (`frontend/index.html`), data adapters (`data_model.py`), dashboard features (`app.py`), validation/tests, and demo/presentation. Use feature branches and pull requests; coordinate edits to `app.py`.

## Checks

```bash
python -m unittest -v test_app
```

Tests cover all six dashboard page renders, saving a wellbeing check-in, marking a task complete, exports, the component navigation event shape, and invalid CSV cases. They do not emulate mouse hover or verify pixel layout. A browser preview could not connect to the build environment's local server, so visual and real iframe click verification remain a local check:

1. Hover each building: outline and detail panel should update.
2. Click a building: its dashboard should open. Return with Base overview.
3. Tab to a building and press Enter; try the side-panel button too.
4. Try the sample CSV, change crew/date, save a check-in, and export it.
5. Resize the browser to check the stacked mobile layout.
