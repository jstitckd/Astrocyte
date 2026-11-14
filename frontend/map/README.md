# Seven-zone habitat map

An original SVG scene with seven distinct spaces. `views/home.py` displays it through `components/base_map.py`.

| ID | Structure | Destination |
| --- | --- | --- |
| `living` | Three-module crew hub, common facilities and communications mast | `views/living.py` |
| `life_support` | Utility module, tanks and pipework | `views/life_support.py` |
| `science` | Laboratory, workshop, dish and rover | `views/science.py` |
| `exercise` | Long training module with panoramic windows | `views/exercise.py` |
| `power` | Solar banks, battery cabinet and service conduit | `views/power.py` |
| `greenhouse` | Glazed growing hall with planted rows | `views/greenhouse.py` |
| `launch` | Separate lander pad, access gantry and spacecraft | `views/launch.py` |

## Edit the design

- `index.html`: terrain, links, structures and label positions. Each numbered structure is in a commented `<g class="building" data-area="...">`; edit its `translate(x y)` to move it. Update any connecting paths when moving a structure.
- `map.css`: appearance, hover/focus highlights, responsive guide and details card. The outer map has no border, and label text has no stroke outline.
- `map.js`: preview, touch and keyboard behaviour, and the Streamlit message bridge.
- `models/areas.py`: `HABITAT_AREAS` is the source of truth for full names, short labels, numbers, categories, descriptions and facility tags. The SVG's `data-area` IDs must match it.

Common artwork is in SVG symbols `cabin`, `water-tank`, `solar-bank` and `stone`. Each zone combines those with its own geometry. The greenhouse and lander have dedicated drawings. There are no image files, external fonts, CDNs or build tools required for the map.

The main purple comes from `theme.primaryColor` in `.streamlit/config.toml`. The illustration's warm terrain, green glass and blue solar panels are separate materials; selection uses a purple footprint highlight without recolouring the structures.

## Interaction

Hover or keyboard focus highlights a building. Clicking a building opens its page; Enter and Space also work. The Explore the outpost panel, guide list and detail card have been removed, and the illustration fills the available width.

On touch screens, tap a building to open its page directly. Reduced-motion preferences disable hover transitions.

The component sends `{area, event_id}` to Python. The wrapper validates the habitat ID and rejects a replayed event, so returning home does not reopen the last selection. The seven target pages are title-only workspaces for the team. Existing crew navigation and old health pages are preserved.
