# Architecture

Astrocyte is a single Streamlit app with a small static JavaScript component for the map. `app.py` loads the shared CSS, renders the sidebar and dispatches `st.session_state.page` to a view's `render()` function.

## Interface

- `views/home.py` lays out crew cards, the map and one environmental panel.
- `views/Alex.py`, `Petrov.py`, `Amara.py` and `Milou.py` load their CSV records, calculate the existing composite score and render the header before the charts. Profile data paths are anchored to the checkout, not the launch directory.
- `components/astronaut_controls.py` provides summary and test-entry dialogs. Their data and test catalogue come from `services/astronaut_tools.py`. Test submission does not write records.
- `views/task_guide.py` renders the selected task's preparation and instruction card. Guide content is in `models/task_guides.py`.
- Registered habitat/older health destinations remain title-only views; they are not full monitoring systems.

## Data and state

`services/dashboard_weather.py` selects the noon row from the supplied hourly CSV and adds deterministic cabin gas values from `services/environment.py`. A reading retains its value, units and `csv`, `demo` or `missing` source. `services/environment_colours.py` defines configurable gauge scales; `components/environment_gauge.py` draws them.

`services/dashboard.py` supplies current crew snapshots and sample assignments. The displayed dashboard scores come from `models/astronauts.py`; the profile composite scores are computed independently in each profile module. They are separate implementations, not a shared clinical model.

Tasks are completed through `completed_habitat_tasks` in Streamlit session state. There is no database, authentication or cross-user task synchronization. Cached CSV reads are read-only.

## Map

`components/base_map.py` serves `frontend/map/` as a Streamlit custom component and passes habitat metadata, pending tasks, accent and background colours. Hover/focus or building clicks select a region. Task buttons post `{area, task, event_id}`; Python validates the assignment and prevents event replay before opening its guide. Multiple tasks at one building stack without covering each other.

## Styling

`frontend/styles.css` defines the shared font, page background and card surface. `frontend/dashboard.css` handles homepage cards; `frontend/astronaut_controls.css` and the dialog styles handle profile controls. Profile modules retain their own layout and Plotly styling. The map iframe has its own stylesheet and font import.

There are no background workers or external measurement APIs. See [data/README.md](../data/README.md) for provenance and [deployment.md](deployment.md) for hosting.
