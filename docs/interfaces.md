# Shared interfaces — agree here before changing another teammate's code

Person 3 integrates changes to `app.py` and `models/areas.py` after the team agrees on a contract change. Each owner can develop against the examples below. Run commands from the repository root.

## Person 2 → everyone: readings

`models/metrics.py` is the single source of truth for accepted numeric metrics, labels, units and aggregation meanings. `models/areas.py` describes building IDs, dashboard metric IDs and default tasks. IDs are stable strings, independent of display labels.

```python
from services.ingestion import validate_readings, filter_readings
frame = validate_readings([{
    "timestamp": "2026-11-14T08:00:00Z", "crew_id": "crew-01",
    "metric": "heart_rate", "value": 64, "unit": "bpm",
    "data_source": "wearable-export",
}])
# pandas.DataFrame with these six columns; timestamp dtype is UTC.
filtered = filter_readings(frame, "crew-01", "2026-11-14", "2026-11-14")
# Includes the entire end date in UTC; returns a new frame.
```

`load_csv(bytes) -> DataFrame` parses UTF-8 CSV (maximum 5 MB) and calls the same validator. Invalid input raises `DataValidationError` with a user-readable message, never partially replaces the loaded dataset. See `docs/data-contract.md` for the complete contract.

`ReadingAdapter.fetch() -> DataFrame` is the future external-provider interface in `services/adapters.py`. Call `read_adapter(adapter)` to validate its output. No network request runs by default.

## Person 2 → Person 3: session store

`SessionStore(st.session_state)` stores imported readings, check-ins, task completion and per-crew EVA checklists. It never mixes check-ins into sensor readings.

```python
store.save_checkin("crew-01", "wellbeing", "2026-11-14", "demo",
                   {"mood": 4, "stress": 2, "notes": "Slept well"})
# Returns a record with id, created_at UTC, date, crew_id, area,
# dataset_id and fields. Validates the fields before saving.
store.set_task("demo", "crew-01", "2026-11-14", "sleep", "review", True)
store.task_done("demo", "crew-01", "2026-11-14", "sleep", "review")  # True
store.export_json()  # UTF-8 JSON bytes, all crew and datasets in this session
```

Imports get a SHA-256 dataset ID; tasks/check-ins are scoped to dataset, crew, date and area. Reimporting identical bytes preserves that dataset's workflow; importing different bytes gives a separate workflow. A saved check-in has an observation date and a separate creation timestamp.

## Person 1 → Person 3: interactive map

`components/base_map.py: render_base_map(selected=None) -> dict | None` loads `frontend/map/index.html`. Python passes the area list and tasks into the component; JavaScript returns `{"area": "sleep", "event_id": "unique-per-activation"}`. `services/navigation.py: destination(event, last_event_id)` validates the ID against `AREAS` and rejects duplicate activations. `app.py` sets the shared `page` session key and reruns. Sidebar controls use the same area IDs.

Person 1 owns the map's drawing and interaction, plus `frontend/styles.css` and `views/home.py`. Hover/focus previews tasks, clicking/Enter/Space opens the area, and touch taps select it; the visible preview button opens it. The map contains no separate list of health tasks: it receives the registry from Python.

## Person 3 → entry point: views

`views/home.py: render_home(context)` and `views/dashboard.py: render_dashboard(context, area_id)` take `components/context.py: ViewContext`. It contains `readings` (filtered), `all_readings`, `crew_id`, `start_date`, `end_date`, `dataset_id`, and `store`. Components own common metric cards, charts, checklists and forms. Views render UI and return no data. Forms call the store; ingestion and validation have no Streamlit dependency.

## Extending without unrelated edits

- New metric: Person 2 adds a `Metric` entry to `models/metrics.py`, synthetic rows in `services/demo.py`, and a validation test. Assign it to an area's `metrics` tuple in `models/areas.py` with Person 3.
- New dashboard/building: add an `Area` in `models/areas.py` and the corresponding labelled SVG region in `frontend/map/index.html` (matching `data-area`). The sidebar and generic dashboard read the registry automatically. Person 3 adds a form if that area needs a new form type.
- New API: implement `ReadingAdapter` and test it with a fixture. Integrate the loader in `components/sidebar.py` only when a real provider and credentials are available.
- New task: update that area's tasks in `models/areas.py`; map previews, checklists and progress use the same definition.

No directory named `pages/` is used: navigation is explicit, so Streamlit cannot automatically add duplicate routes.
