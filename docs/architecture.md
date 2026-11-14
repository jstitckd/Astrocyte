# Template architecture

The app is a navigation shell with an editable interactive homepage map and seven blank destination pages. Shared branding, navigation and theme remain. There are no active health features or data services.

## File responsibilities

| Path | Purpose |
| --- | --- |
| `app.py` | Configures Streamlit, loads CSS and calls the selected page's `render()`. |
| `components/sidebar.py` | Sidebar logo and navigation buttons. |
| `models/areas.py` | Names and icons for the six habitat areas. |
| `models/metrics.py` | Empty `METRICS` dictionary for the team to define. |
| `views/home.py` | Displays the map and navigates to its selected area. |
| `views/sleep.py` | Blank sleeping-quarters page. |
| `views/exercise.py` | Blank exercise page. |
| `views/medical.py` | Blank medical-bay page. |
| `views/nutrition.py` | Blank kitchen page. |
| `views/wellbeing.py` | Blank greenhouse / common-room page. |
| `views/eva.py` | Blank airlock / EVA page. |
| `views/data.py` | Blank data page; no imports or exports are implemented. |
| `frontend/styles.css` | Minimal shared layout, branding and navigation styling. |
| `frontend/map/` | Editable SVG drawing (`index.html`), map styling (`map.css`) and interactions (`map.js`). |
| `components/base_map.py` | Streamlit component wrapper; passes names to the map and validates/deduplicates navigation events. |
| `services/` | Workspace for future data, validation, storage and APIs. |
| `data/` | Workspace for your own safe datasets. |
| `tests/test_app.py` | Blank-page navigation integration tests. |
| `.streamlit/config.toml` | Safe theme and Streamlit settings. |
| `Astrocyte.code-workspace` | Project interpreter and debug launcher. |
| `requirements.txt` | Existing runtime packages, available as the team builds features. |

There is no `pages/` directory because navigation is explicit. The old shared `views/dashboard.py` has been removed: every area now has its own file. Old data services, sample readings and health widgets have also been removed. The homepage now has a small editable map starter.

## Navigation

Sidebar button → updates `st.session_state.page` → Streamlit reruns `app.py` → `VIEWS[page]()` calls the selected page's `render()`.

Map click or keyboard activation → JavaScript sends `{area, event_id}` → `components/base_map.py` checks the message → `views/home.py` sets `st.session_state.page` and reruns the app.

An unknown page ID returns to `home`. A repeated map event is ignored so returning home does not reopen the last building. The template keeps only navigation state; it loads and saves no health data.

## Adding your own content

Edit a page's `render()` function. Import reusable elements from `components/` and data logic from `services/` when your team implements those modules.

To add another habitat area: add its name/icon to `models/areas.py`, create `views/your_page.py` with `render()`, import it in `app.py`, and add its ID/function to `VIEWS`. Update the navigation tests when you introduce content or new destinations.

## Historical guide

`docs/code-layout-guide.html`, if present, describes the previous full prototype and is preserved unchanged. It is not the current architecture. The previous implementation is available from Git commit `aef6f9d` if the team wants to reuse a piece later.
