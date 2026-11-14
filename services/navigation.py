"""Validate component messages before using them as application navigation."""
from models.areas import AREAS


def destination(event, last_event_id):
    if not isinstance(event, dict):
        return None
    area = event.get("area")
    event_id = event.get("event_id")
    if not isinstance(area, str) or area not in AREAS:
        return None
    if not isinstance(event_id, str) or not event_id or len(event_id) > 120 or event_id == last_event_id:
        return None
    return area
