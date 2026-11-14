# Reusable interface elements

`sidebar.py` supplies the shared branding and working navigation. Add reusable charts, forms, cards or map wrappers here as the team builds them, and import them from your page in `views/`.

`base_map.py` embeds the HTML map and returns a validated page ID once per activation. It is called from `views/home.py`.

No dashboard widgets or data workflows are included in this template.
