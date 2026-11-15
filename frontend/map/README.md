# Habitat map component

- `index.html`: original SVG illustration and explicit roof anchor points.
- `map.css`: appearance, IBM Plex Sans, task positions and urgency styles.
- `map.js`: Streamlit bridge, selection, task guide clicks and connectors.
- `models/areas.py`: the seven habitat IDs, labels and metadata supplied by Python.

Buildings highlight on hover, focus, click or keyboard activation; these actions do not navigate. Task cards open their task guide. Yellow left edges/badges mean pending and red means urgent. No icon or map reading establishes that a habitat is safe to enter.

Task card placement is controlled by `.task-living`, `.task-science` and `.task-exercise`. `circle.task-anchor` coordinates (`cx`/`cy`) in the matching SVG building choose the roof attachment point. `drawTaskConnectors()` scales those points to the scene. The first exercise card has a horizontal connector; additional cards for the same building stack below it.

Python passes pending tasks and registered areas into the component. Task clicks send `{area, task, event_id}`. `components/base_map.py` validates the message and ignores a replayed event before changing the Streamlit route. Keep the IDs in the registry and SVG `data-area` attributes synchronized.

The illustration requires no image downloads or build tools. Google Fonts is an external request; the supplied font fallback remains usable without it.
