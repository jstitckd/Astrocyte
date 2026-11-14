# Data contract workspace

The blank template does not load demo readings, import files, save records or connect to external APIs. No metric schema or provider interface is implemented. `models/metrics.py` starts with an empty dictionary.

Before adding data, agree on:

- Stable crew and metric IDs, units and source labels.
- Timestamp format and timezone interpretation.
- Whether records are individual measurements, events or daily totals.
- Validation errors and duplicate handling.
- Separation of imported measurements from self-reported entries.
- Storage ownership, persistence and export behaviour.

Put shared definitions in `models/`, processing and storage in `services/`, safe sample files in `data/`, reusable controls in `components/` and the import/export interface in `views/data.py`.

Keep provider keys outside Git, in environment variables or `.streamlit/secrets.toml`. No credentials are needed to run the skeleton.

The former six-column CSV importer and synthetic sample were removed. They are available in Git history at commit `aef6f9d` as a reference if the team decides to reuse them.
