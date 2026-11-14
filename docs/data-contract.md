# Reading contract, version 1

CSV headers are case-sensitive. Required columns (additional columns are ignored):

| Column | Meaning |
| --- | --- |
| `timestamp` | ISO 8601 date and time, e.g. `2026-11-14T08:00:00Z`. Offsets are normalized to UTC. Missing offsets mean UTC, never the laptop's local timezone. Date-only/ambiguous local formats are rejected. |
| `crew_id` | Stable ID, 1–64 letters/digits/`_`/`.`/`-`, starting with a letter or digit; e.g. `crew-01`. Display names are optional mappings in `models/metrics.py`. |
| `metric` | One of the exact IDs below. |
| `value` | A finite number; no missing, text, boolean, NaN or infinite values. Non-temperature values must be non-negative. This is data-integrity validation, not clinical interpretation. |
| `unit` | Exact unit below; no automatic unit conversion. Celsius uses the Unicode degree symbol in UTF-8. |
| `data_source` | Nonblank descriptive provenance, e.g. `wearable-export`, `synthetic-sensor`, `synthetic-daily-log`. A source name does not establish device accuracy. |

Text fields are trimmed and limited to 120 characters; control characters are rejected. Maximum file size is 5 MiB, maximum row count is 50,000. Empty datasets and duplicates of `(crew_id, timestamp, metric)` are rejected, even when data sources differ. The entire file is validated before replacing the active import. Unknown metrics and wrong units produce an explanation beside the uploader.

| Metric ID | Unit | Record meaning |
| --- | --- | --- |
| `heart_rate` | `bpm` | Individual resting measurement; the app does not establish that an uploaded measurement was taken overnight. |
| `hrv` | `ms` | Individual RMSSD measurement; adapters must convert or reject other HRV definitions. |
| `sleep_hours` | `h` | Total duration of the sleep episode ending on the timestamp's date. |
| `spo2` | `%` | Individual peripheral oxygen saturation reading. |
| `body_temperature` | `°C` | Individual body-temperature measurement. |
| `activity_minutes` | `min` | Daily activity total. |
| `exercise_heart_rate` | `bpm` | Individual measurement during exercise. |
| `fluid_ml` | `mL` | Daily logged fluid total, not a sensor inference. |
| `energy_kcal` | `kcal` | Daily logged energy total, not a sensor inference. |
| `eva_minutes` | `min` | Daily EVA duration total. |
| `radiation_msv` | `mSv` | Daily dosimeter exposure total, not cumulative mission exposure. |

Daily totals permit **one row per crew, UTC date and metric**. If a provider supplies events or partial totals, its adapter must produce a final daily total first. Do not sum cumulative totals. These conventions avoid double-counting. Individual measurements are plotted as supplied; the prototype does not resample, fill missing values, infer medical thresholds or issue health alerts. Latest cards select the final timestamp within the current crew/date window.

## Example

```csv
timestamp,crew_id,metric,value,unit,data_source
2026-11-14T08:00:00Z,crew-01,heart_rate,64,bpm,wearable-export
2026-11-14T23:59:00Z,crew-01,fluid_ml,2400,mL,manual-daily-total
```

`data/sample_readings.csv` contains deterministic synthetic records for the whole demo. To regenerate after intentionally changing the demo definitions, run from the root:

```bash
python -c "from services.demo import demo_readings; from services.ingestion import readings_csv; from pathlib import Path; Path('data/sample_readings.csv').write_bytes(readings_csv(demo_readings()))"
```

## Future API adapter

```python
import pandas as pd
from services.adapters import read_adapter

class FixtureAdapter:
    def fetch(self) -> pd.DataFrame:
        # A fixture example, not an implemented wearable connection.
        return pd.DataFrame([{
            "timestamp": "2026-11-14T08:00:00Z", "crew_id": "crew-01",
            "metric": "heart_rate", "value": 64, "unit": "bpm",
            "data_source": "adapter-fixture",
        }])

frame = read_adapter(FixtureAdapter())  # validated, sorted UTC DataFrame
```

A real adapter handles authentication, timeouts, rate limits, source-specific units and IDs, then returns this schema. Keep keys in `st.secrets`/environment variables in that adapter's integration layer; do not embed keys in source. No provider is selected or contacted by the app today.

## Check-ins and tasks are a different contract

Check-ins contain `id`, `created_at` (UTC), `date` (observation date), `crew_id`, `area`, `dataset_id` and a `fields` dictionary. Fields hold self-reported notes, symptoms, mood/stress ratings, exercise duration or nutrition entry amounts. They do **not** become reading rows. Mood and stress use a user-selected 1–5 scale without an automated conclusion.

Nutrition forms log individual entry amounts; their values are never added to imported daily totals. Tasks have their own dataset/crew/date/area scope and a map of task IDs to booleans. They describe manual completion, not a sensor's judgement of readiness or health.

Session JSON exports all these records plus per-crew EVA checklist configuration. It is an archive only; no JSON restore workflow is implemented. Measurement CSV exports round-trip through the CSV validator. The UI exports the selected reading window; no hidden aggregation takes place.
