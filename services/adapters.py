"""Implement this boundary when the team chooses a real data provider."""
from typing import Protocol

import pandas as pd

from services.ingestion import validate_readings


class ReadingAdapter(Protocol):
    def fetch(self) -> pd.DataFrame:
        """Return timestamp, crew_id, metric, value, unit, data_source columns."""
        ...


def read_adapter(adapter: ReadingAdapter) -> pd.DataFrame:
    """Adapters may fetch; only validated data crosses into the application."""
    return validate_readings(adapter.fetch())
