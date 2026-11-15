# Verification

Use the pinned dependencies and Python 3.12:

```bash
python -m unittest discover -s tests -v
git diff --check
```

The suite checks navigation, task guides and completion, crew summaries, profile dialogs, unchanged CSVs after mock submission, header-before-chart rendering, weather units and missing readings, gauge bounds and display colours. Test counts can change as features evolve.

GitHub Actions runs this suite on Linux. Before release, also run the app and inspect the dashboard, every profile, both dialogs, task guides and task completion in a desktop browser. Verify the custom map loads and the new-session state resets. Python tests do not replace browser rendering checks.

The repository includes no generated browser screenshots or old prototype reports. Tests should use the bundled synthetic fixtures and should not require credentials, private health records or external measurement APIs.
