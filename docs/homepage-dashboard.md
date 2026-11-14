# Homepage dashboard

Run `.venv/bin/python -m streamlit run app.py` from the Astrocyte folder.

| Change | File |
| --- | --- |
| Main layout and task list | `views/home.py` |
| Reading cards and crew summary markup | `components/dashboard.py` |
| Card spacing, colours, sizes and mobile layout | `frontend/dashboard.css` |
| CSV snapshot loading and sample assignments | `services/dashboard.py` |
| Cabin demo formulas and optional CSV channels | `services/environment.py` |
| Habitat illustration and marker styling | `frontend/map/index.html`, `frontend/map/map.css` |
| Marker clicks and map interactions | `frontend/map/map.js` |
| Streamlit map bridge | `components/base_map.py` |

Cabin cards use the existing synthetic `testing.py` scenario when the weather CSV has no cabin measurements. Optional cabin channels supplied in the environmental CSV take precedence; see `docs/environment.md`. Outside readings come from the recorded noon Mars observation. These are snapshots, not a live sensor connection. Cached snapshots refresh on a subsequent page run after 30 seconds.

Crew summaries read the latest rows of `data/alex.csv`, `data/petrov.csv` and their corresponding `_30days.csv` files. The ring is the CSV's sleep score, not a calculated overall health score. All current crew files are synthetic. Heart rate and SpO₂ are the latest daily measurements; HRV and sleep score are the latest recovery record.

Sample tasks are assigned to a crew member and habitat area in `SAMPLE_TASKS`. Assigned tasks and **Mark complete** buttons appear inside each crew health card above the map. Clicking a map notification opens a dedicated learning page with preparation, numbered steps, reference links where applicable, and completion/return controls. Edit the instructions in `models/task_guides.py` and the page layout in `views/task_guide.py`. Completing a guide marks the same session task complete and returns to the dashboard. Completed tasks disappear from the map and the counts update. Completion persists through navigation in the same Streamlit session. New sessions start with all sample tasks. There is no shared task database, email or push notification service.

Building clicks still open the existing habitat pages. The crew summary buttons open Alex and Petrov's existing pages. The map stays unboxed, with the environment readings in a column on its right.
