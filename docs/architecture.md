# Blank template architecture

The app is a navigation shell with eight empty pages. Only the sidebar branding, navigation, theme and page titles are rendered. There are no active health features or data services.

## File responsibilities

| Path | Purpose |
| --- | --- |
| `app.py` | Configures Streamlit, loads CSS and calls the selected page's `render()`. |
| `components/sidebar.py` | Sidebar logo and navigation buttons. |
| `models/areas.py` | Names and icons for the six habitat areas. |
| `models/metrics.py` | Empty `METRICS` dictionary for the team to define. |
| `views/home.py` | Blank homepage. |
| `views/sleep.py` | Blank sleeping-quarters page. |
| `views/exercise.py` | Blank exercise page. |
| `views/medical.py` | Blank medical-bay page. |
| `views/nutrition.py` | Blank kitchen page. |
| `views/wellbeing.py` | Blank greenhouse / common-room page. |
| `views/eva.py` | Blank airlock / EVA page. |
| `views/data.py` | Blank data page; no imports or exports are implemented. |
| `frontend/styles.css` | Minimal shared layout, branding and navigation styling. |
| `frontend/map/` | Workspace for your future map assets. |
| `services/` | Workspace for future data, validation, storage and APIs. |
| `data/` | Workspace for your own safe datasets. |
| `tests/test_app.py` | Blank-page navigation integration tests. |
| `.streamlit/config.toml` | Safe theme and Streamlit settings. |
| `Astrocyte.code-workspace` | Project interpreter and debug launcher. |
| `requirements.txt` | Existing runtime packages, available as the team builds features. |

There is no `pages/` directory because navigation is explicit. The old shared `views/dashboard.py` has been removed: every area now has its own file. Old data services, sample readings, widgets and map assets have also been removed to give the team a blank starting point.

## Navigation

Sidebar button → updates `st.session_state.page` → Streamlit reruns `app.py` → `VIEWS[page]()` calls the selected page's `render()`.

An unknown page ID returns to `home`. The only application state the skeleton uses is the current page; it loads and saves no health data.

## Adding your own content

Edit a page's `render()` function. Import reusable elements from `components/` and data logic from `services/` when your team implements those modules.

To add another habitat area: add its name/icon to `models/areas.py`, create `views/your_page.py` with `render()`, import it in `app.py`, and add its ID/function to `VIEWS`. Update the navigation tests when you introduce content or new destinations.

## Historical guide

`docs/code-layout-guide.html`, if present, describes the previous full prototype and is preserved unchanged. It is not the current architecture. The previous implementation is available from Git commit `aef6f9d` if the team wants to reuse a piece later.
