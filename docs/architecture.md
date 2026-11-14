# Current habitat-map architecture

`app.py` dispatches views and loads the shared purple branding. Existing crew pages and older health routes remain available. The homepage now has a seven-zone SVG habitat map, each with a title-only destination for the team to build on.

| File | Responsibility |
| --- | --- |
| `views/home.py` | Displays the map and handles its selected destination. |
| `components/base_map.py` | Passes metadata/accent into the iframe; validates and deduplicates returned navigation messages. |
| `models/areas.py` | `HABITAT_AREAS` defines all seven spaces; original `AREAS` preserves older pages. |
| `frontend/map/index.html` | Original isometric artwork: terrain, habitat links, service road and seven distinct facilities. |
| `frontend/map/map.css` | Borderless map, labels, focus/hover highlights, space guide and mobile layout. |
| `frontend/map/map.js` | Preview, accessible activation, mobile guide and Streamlit messaging. |
| `views/living.py` | Main living and working quarters. |
| `views/life_support.py` | Environmental control and life support. |
| `views/science.py` | Labs and maintenance workshops. |
| `views/exercise.py` | Exercise quarters; retains the existing exercise route. |
| `views/power.py` | Power generation and storage. |
| `views/greenhouse.py` | Greenhouse. |
| `views/launch.py` | Spaceship and launch area. |
| `components/sidebar.py` | Existing logo and crew navigation. |
| `views/Alex.py`, `models/astronauts.py` | Team-owned crew work, preserved. |
| `views/data.py` | Existing blank data page. |
| `frontend/styles.css` | Shared page/brand styling; the user's logo spacing is retained. |
| `tests/test_app.py` | Map/page contracts, legacy route smoke checks and crew navigation. |

The older sleep, medical, nutrition, wellbeing and EVA view files are retained. The new map does not overwrite or repurpose them. There is no Streamlit automatic `pages/` directory.

## Flow

The component receives all copy from `HABITAT_AREAS`. Hover/focus updates a local description card and selects the matching guide row. Activation sends `{area, event_id}` to Python. The validated area is placed in `st.session_state.page`, then Streamlit reruns and displays its registered view.

Only navigation state is added by the map. No health scores, system statuses, live data or operational readiness conclusions are generated. Descriptions explain the roles of concept facilities.

## Working on it

For illustration/styling, edit the commented zone groups in `frontend/map/index.html` and `map.css`. For page content, edit that zone's own view. For copy and labels, change `HABITAT_AREAS`. Adding a zone requires a registry entry, SVG region, registered view and updated integration/browser checks.

See `frontend/map/README.md` for exact IDs and interaction behaviour. `docs/code-layout-guide.html` is historical documentation for an earlier prototype and does not describe this map revision.
