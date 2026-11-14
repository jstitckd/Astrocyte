# Data and storage workspace

`environment.py` adapts the environmental CSV parser and synthetic cabin formulas from `testing.py` for the homepage. It validates recorded snapshots, keeps measured/demo/missing provenance and converts display units. It makes no network requests and saves no records.

See `docs/environment.md` for supported columns, source limitations and the optional cabin-demo toggle. Add future loading, storage and provider modules here, separate from the interface.

Agree on inputs and outputs with the page owners first. Put shared metric definitions in `models/metrics.py` and datasets in `data/`. Keep keys in environment variables or `.streamlit/secrets.toml` (ignored by Git).
