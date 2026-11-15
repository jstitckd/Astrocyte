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

Dashboard outside temperature, pressure and UV come from `data/mars_diurnal_weather_radiation-v2.csv`, copied from the supplied file. `services/dashboard_weather.py` selects the 12:00 row: −32.0 °C, 504.8 Pa and UV index 51. The radiation card displays **UV index**, not ionising-radiation dose or µSv/h. The file's risk labels are not used to make safety judgements. Missing or invalid readings remain unmeasured.

Cabin O₂ and CO₂ retain the existing synthetic `testing.py` scenario (Sol 1740); the new CSV has no cabin gas channels. These are snapshots, not a live sensor connection. Cached snapshots refresh on a subsequent page run after 30 seconds. To select another observation, change the `time` argument passed to `weather_snapshot()` in `services/dashboard.py`. The detailed legacy environmental component remains separate; see `docs/environment.md`.

Environment cards with multiple recorded samples include a tiny SVG image styled with a purple line, faded area and selected-time dot. Temperature, pressure and UV use the hourly CSV profile; missing samples remain gaps. Cabin gases have no graph, since they have no measured history. Cards are ordered radiation/UV, outside temperature, outside pressure, cabin O₂, then cabin CO₂. Hover over a graph for its series description and selected time. Each chart scales independently. Edit the drawing in `components/environment_sparkline.py` and its size in `frontend/dashboard.css` (`.env-sparkline`).

Crew summaries read the latest rows of `data/alex.csv`, `data/petrov.csv` and their corresponding `_30days.csv` files. The ring is the CSV's sleep score, not a calculated overall health score. All current crew files are synthetic. Heart rate and SpO₂ are the latest daily measurements; HRV and sleep score are the latest recovery record.

Sample tasks are assigned to a crew member and habitat area in `SAMPLE_TASKS`. Assigned tasks and **Mark complete** buttons appear inside each crew health card above the map. Clicking a map notification opens a dedicated learning page with preparation, numbered steps, reference links where applicable, and completion/return controls. Edit the instructions in `models/task_guides.py` and the page layout in `views/task_guide.py`. Completing a guide marks the same session task complete and returns to the dashboard. Completed tasks disappear from the map and the counts update. Completion persists through navigation in the same Streamlit session. New sessions start with all sample tasks. There is no shared task database, email or push notification service.

Building clicks still open the existing habitat pages. The crew summary buttons open Alex and Petrov's existing pages. The map stays unboxed, with the environment readings in a column on its right.

## Environmental icon colours

Edit `services/environment_colours.py` to change the display bands. Icons and mini graphs use the same colour. Hover over a card for the category; screen readers receive the same description.

| Channel | Display colours |
| --- | --- |
| UV index | Green below 3; amber from 3 to below 6; red from 6 upward, retaining High / Very high / Extreme text categories. |
| Outside temperature | Blue below freezing; amber at or above freezing. |
| Outside pressure | Amber below 1,000 Pa; blue otherwise. This describes outside pressure, not cabin pressure. |
| Cabin O₂ | Green from 19.5–23.5%; red outside that range. |
| Cabin CO₂ | Green below 1,000 ppm; amber from 1,000 to below 5,000; red from 5,000. |
| Missing values | Grey. |

UV category boundaries follow the [EPA UV-index guide](https://www.epa.gov/sites/default/files/documents/uviguide.pdf). Red for High and above is a design choice. The oxygen concentration band references [OSHA's confined-space definitions](https://webapps.dol.gov/elaws/osha/confined/definitions.asp). These Earth-based bands are visual reference points, not validated spacecraft alarm limits or an EVA clearance. Temperature, outside-pressure and CO₂ colour bands are configurable display choices. In particular, the [NIOSH CO₂ 5,000 ppm limit](https://www.cdc.gov/niosh/npg/npgd0103.html) is a time-weighted exposure limit, not an instantaneous safety threshold; the dashboard does not compute exposure duration or certify air quality.

## Task urgency colours

Set `urgent: True` on an assignment in `services/dashboard.py` to make it urgent. Pending tasks use yellow outlines and due text; urgent tasks use red. Map connectors use the same colours. A crew badge is red if any pending task is urgent, yellow if pending tasks are all non-urgent, and green when there are no pending tasks. Completion recalculates these colours automatically. The colours are `--task-due` and `--task-urgent` in `frontend/dashboard.css` and `frontend/map/map.css`; changing the brand accent does not change task urgency colours.
