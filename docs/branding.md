# Branding and theme

- **Font:** IBM Plex Sans, loaded from Google Fonts with Arial/sans-serif fallbacks.
- **Accent:** `#d093f6`, configured by `theme.primaryColor` in `.streamlit/config.toml`.
- **Page background:** `#0b0f12`.
- **Card surface:** gradient from `#141b1f` to `#11171b`.
- **Raised task surface:** `#1d272d`.

The sidebar wordmark is live text plus the team-supplied purple symbol in `frontend/astrocyte-mark.png`. `components/sidebar.py` frames that PNG in an SVG and filters neutral residue; `frontend/styles.css` sets its dimensions and typography. Replacing the symbol with a different crop may require changing `_brand_mark()`'s SVG viewport.

The map iframe uses `frontend/map/map.css`. Its terrain, glass and solar-panel colours are illustration materials, independent of the purple brand accent. Task urgency uses yellow/red independently of that accent.

See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for font, flag, logo and data attribution/provenance.
