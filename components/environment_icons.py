"""Small, consistent vector icons for the dashboard's environmental cards."""
import base64
from functools import lru_cache
import re


ICONS = {
    "uv_index": '<circle cx="12" cy="12" r="2.1" fill="currentColor" stroke="none"/>' + ''.join(
        f'<path transform="rotate({angle} 12 12)" d="M9.5 7.67 7 3.34A10 10 0 0 1 17 3.34L14.5 7.67A5 5 0 0 0 9.5 7.67Z" fill="currentColor" stroke="none"/>'
        for angle in (0, 120, 240)
    ),
    "air": '<path d="M10 14.5V5a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0Z"/><path d="M12 8v10m5-11h3m-3 4h2"/><circle cx="12" cy="18" r="2" fill="currentColor" stroke="none"/>',
    "pressure": '<circle cx="12" cy="12" r="9"/><path d="m12 12 4.5-4.5M5 12h2m10 0h2M12 5v2m-5-2 1.4 1.4M7 19h10"/><circle cx="12" cy="12" r="1.7" fill="currentColor" stroke="none"/>',
    "o2": '<path d="M12 3v8m0-3-3 4m3-4 3 4M9 7C6 8 3 13 3 17c0 4 6 4 6 1V7Zm6 0c3 1 6 6 6 10 0 4-6 4-6 1V7Z"/>',
    "co2": '<circle cx="12" cy="12" r="3.5"/><circle cx="3.5" cy="12" r="2.5"/><circle cx="20.5" cy="12" r="2.5"/><path d="M6 11h2.5M6 13h2.5m7-2H18m-2.5 2H18"/>',
}


@lru_cache(maxsize=32)
def environment_icon(channel, accent):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
        accent = "#d093f6"
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="color:{accent}">{ICONS[channel]}</svg>'
    encoded = base64.b64encode(svg.encode()).decode("ascii")
    return f'<img class="dash-icon" src="data:image/svg+xml;base64,{encoded}" alt="" aria-hidden="true">'
