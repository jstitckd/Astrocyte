# Reusable interface elements

`sidebar.py` supplies the shared branding and working navigation. Add reusable charts, forms, cards or map wrappers here as the team builds them, and import them from your page in `views/`.

`base_map.py` embeds the HTML map and returns a validated page ID once per activation. It is called from `views/home.py`.

`dashboard.py` renders the compact homepage readings and crew summaries. `environment.py` retains a reusable detailed environmental overview; `environment_charts.py` builds its recorded Plotly profiles. Source data and demo logic live in `services/environment.py`, and the scoped styling is in `frontend/environment.css`. See `docs/environment.md` for provenance and monitoring gaps.
