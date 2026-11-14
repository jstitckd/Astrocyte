from dataclasses import dataclass
from datetime import date

import pandas as pd

from services.storage import SessionStore


@dataclass
class ViewContext:
    readings: pd.DataFrame
    all_readings: pd.DataFrame
    crew_id: str
    start_date: date
    end_date: date
    dataset_id: str
    store: SessionStore

    @property
    def is_demo(self):
        return self.dataset_id == "demo"
