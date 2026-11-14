from pathlib import Path

from streamlit.components.v1 import declare_component

from models.areas import AREAS

_map = declare_component("astrocyte_base_map", path=str(Path(__file__).resolve().parents[1] / "frontend" / "map"))


def render_base_map(selected=None):
    areas = [{"id": key, "name": area.name, "code": area.code, "description": area.description,
              "tasks": [task.label for task in area.tasks]}
             for key, area in AREAS.items()]
    return _map(areas=areas, selected=selected, default=None, key="mars_map")
