# Shared page and map interfaces

## Page interface

Views expose `render()` with no arguments. The homepage embeds the habitat map. Seven habitat destinations expose a title and a comment for the team's future content. Existing crew and older health pages remain independent.

To add a route, import its module in `app.py` and register its `render` function in `VIEWS`.

## Habitat registry

`models/areas.py: HABITAT_AREAS` maps the stable IDs `living`, `life_support`, `science`, `exercise`, `power`, `greenhouse`, `launch` to `HabitatArea` instances containing:

- `code`: two-digit map number.
- `name`: full destination title and accessible label.
- `label`: short map/guide label.
- `description`: role shown on hover or focus.
- `features`: tuple of facility tags.
- `category`: short label above the description.

The older `AREAS` registry is retained for legacy page titles. It is not used by the new map. Coordinate shared registry/route changes before editing.

## Map bridge

`components/base_map.py: render_base_map()` returns a newly selected habitat ID or `None`. It passes the registry fields and the configured accent colour into the component.

```text
Python → HTML:
areas=[{id: "living", code: "01", name: "Main living & working quarters",
        label: "Living & working", description: "...", features: [...], category: "..."}, ...]
accent="#d093f6"

HTML → Python:
{area: "living", event_id: "unique-activation-id"}
```

Python validates the area and event ID and ignores the last processed event. `views/home.py` sets `st.session_state.page` and calls `st.rerun()`. SVG regions, `HABITAT_AREAS` and `VIEWS` must agree on IDs; the tests check this connection.

## Crew sidebar

The sidebar uses the team's `models/astronauts.py` registry and preserves the `Alex` route. Habitat navigation is inside the map's space guide; it does not add old building links back into the crew sidebar.

## Future data

The habitat-map change adds no measurements, storage or device integration. Agree on any new data contracts before linking pages to services. Keep imported measurements and self-reported entries distinct.

## Homepage environment interface

See [environment.md](environment.md) for the environmental data contract. `services/environment.py: load_csv(bytes)` returns a normalized frame/schema, and `take_snapshot(frame, schema, sol, time, show_demo)` returns a `Snapshot` with `Reading(value, unit, source, note)` objects. Sources are `csv`, `demo` or `missing`. `converted()` changes display units without modifying raw data.

`components/environment.py: render_environment_overview()` renders cards, controls and expandable profiles before the map. Agree on new recorded channels and add them to the service aliases/units with tests. Environmental values do not modify crew records.
