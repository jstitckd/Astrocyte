# Logo and accent colour

The active sidebar logo combines the original lowercase `astrocyte.` text with the supplied purple astrocyte symbol. It is rendered in `components/sidebar.py`; sizing, spacing and text styling are in `frontend/styles.css`.

- **Symbol source:** `frontend/astrocyte-mark.png`, copied unchanged from the uploaded image.
- **Text:** live text in the site's inherited Source Sans font, 29 px, weight 650, letter spacing −1.3 px.
- **Accent:** `#d093f6`, sampled from the purple symbol.

`_brand_mark()` wraps the supplied bitmap in a small SVG viewport. Its browser colour filter keeps the purple silhouette and hides neutral white/black residue from the cutout. The PNG is not edited, and no external image service or local raster-processing script runs in the app. The icon displays on a transparent background alongside the live text.

The SVG viewport is framed to this particular uploaded mark. If replacing it with a differently shaped or sized source, adjust the viewport and source dimensions in `_brand_mark()`.

To change the main accent, edit `primaryColor` in `.streamlit/config.toml` using a six-digit hex value, then restart Streamlit. `app.py` supplies that colour to the shared CSS, the sidebar wrapper uses it for the symbol, and `components/base_map.py` passes it into the map. This updates the dot, primary buttons, focus states and map highlights together. Mars terrain colours are separate illustration colours in the map files.

The previous full image `frontend/logo.png` is retained as a source reference; it is no longer displayed by the sidebar.
