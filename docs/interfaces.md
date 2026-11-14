# Interfaces for the blank template

## Page interface

Every file in `views/` exposes `render()` with no arguments. It renders Streamlit content and returns nothing. The seven destination pages display only their titles. The homepage also embeds the editable Mars-base map.

```python
import streamlit as st


def render():
    st.title("Your page title")
    # Add your own Streamlit content here.
```

The integration owner imports that module in `app.py` and adds `"your_page": your_page.render` to `VIEWS`.

## Navigation interface

`components/sidebar.py: render_sidebar()` displays navigation. Its buttons call `go(page_id)`, which sets `st.session_state.page`. Six building names/icons are defined in `models/areas.py`; the homepage and data destinations are separate shell routes.

Stable current IDs: `home`, `sleep`, `exercise`, `medical`, `nutrition`, `wellbeing`, `eva`, `data`. Keep these IDs aligned between the sidebar and `app.py`.

## Map component

`components/base_map.py: render_base_map()` returns a newly selected area ID or `None`. The HTML receives `areas=[{"id": "sleep", "name": "Sleeping quarters"}, ...]` and sends `{area: "sleep", event_id: "unique-activation-id"}`. Python validates both fields and ignores the last processed event.

`views/home.py` sets `st.session_state.page` to the returned area ID and calls `st.rerun()`. The map IDs must match `models/areas.py` and `app.py`.

## Future shared data

There is no dataset, `ViewContext`, session store, provider adapter or form contract in this template. Define those together before implementing them. `models/metrics.py`, `services/`, `components/` and `data/` are the intended workspaces.

Before changing arguments or IDs used by another teammate, agree on the new input/output format and update callers and tests together.
