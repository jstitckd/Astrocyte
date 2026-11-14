# Blank template verification

Run from the repository root using the project's environment:

```bash
python -m unittest discover -s tests -v
```

Both integration tests pass on macOS with Python 3.12 using Streamlit AppTest:

1. All eight sidebar destinations render without exceptions and show only their page title in the main content area. No metrics, charts, uploads or export controls are loaded.
2. An unknown saved page ID returns to the homepage.

The previous health-workflow and browser tests were removed together with the features they exercised. Add tests as the team implements its own features, and update the blank-content assertions for pages that gain content.

This template revision was not tested in a real browser, on Windows or on Streamlit Community Cloud. No deployment or GitHub push was performed as part of the blank-template change. The existing `.venv`, workspace launcher and Streamlit entry point are preserved.
