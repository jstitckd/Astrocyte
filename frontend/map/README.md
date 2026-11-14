# Your editable homepage map

The map is displayed by `render_base_map()` in `views/home.py`. The Python-to-JavaScript connection is in `components/base_map.py`.

| File | Edit this to… |
| --- | --- |
| `index.html` | Draw the terrain, paths and buildings. |
| `map.css` | Change colours, highlights, labels and mobile layout. |
| `map.js` | Change hover, keyboard, click and tap behaviour. |

The main accent is supplied by `theme.primaryColor` in `.streamlit/config.toml`, so the logo, navigation and map agree. Change other map colour variables at the top of `map.css`. Move a building by changing its `transform="translate(x y)"` in `index.html`. The `<symbol id="building">` is the reusable building artwork; editing it changes all six modules. You can replace an individual `<use>` with your own SVG shapes for a unique building.

Keep these `data-area` IDs aligned with `models/areas.py`: `sleep`, `exercise`, `medical`, `nutrition`, `wellbeing`, `eva`. Display names come from that Python registry.

On desktop, hover or focus previews the building name; click, Enter or Space opens its page. On mobile, tap a building to open it directly, or choose a labelled button and then use Open page. The sidebar is always available.

The component sends `{area, event_id}` back to Python. The wrapper validates the ID and ignores a repeated event, so returning to the homepage does not immediately reopen the previous building.
