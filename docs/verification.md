# Verification

## Python checks

Verified on macOS arm64 with Python 3.12.12 in a newly created `Astrocyte/.venv`. Installed the pinned `requirements.txt` into that empty environment, launched Streamlit successfully, and ran:

```bash
python -m unittest discover -s tests -v
python -m pip check
```

**17 tests pass**; `pip check` reports no broken requirements. Coverage includes:

- The committed synthetic sample matches the generator and CSV exports round-trip.
- Offsets normalize to UTC; naive timestamps mean UTC; the entire end date is included in filtering.
- Missing/unknown columns and metrics, wrong units, invalid/numeric/ambiguous dates, nonnumeric/nonfinite values, duplicate rows, duplicate daily totals and oversize/unreadable CSVs are rejected.
- A future adapter passes through the same validation boundary, including already-normalized timestamp columns.
- Invalid imports leave the last valid dataset intact. Identical bytes preserve dataset identity.
- Check-ins stay separate from readings and respect dataset, crew, area and date scopes.
- Check-in field validation, custom EVA lists and per-day/per-crew task persistence work.
- Every sidebar route renders, and each of the six map-event destinations resolves to its own dashboard.
- All six form types accept valid entries; empty observations show a helpful error.
- Crew/date filters reach the displayed dataset; imported data reaches cards and Plotly components; missing imports show an empty state and disable saving.
- Task completion survives navigation and reaches homepage progress; sample/reading/session export controls exist.

The fresh environment was created with the installed Python 3.12 interpreter, then dependencies installed using the same `python -m pip install -r requirements.txt` command documented in the README. The app runs with `python -m streamlit run app.py` from the repository root. No pre-existing app dependencies were reused.

## Real-browser checks

The optional `tests/browser_smoke.py` uses headless Chrome through Playwright. Tested at desktop 1512 × 1100 and mobile-emulated 390 × 844 with touch enabled:

- Local page returns HTTP 200 and renders the original SVG map.
- Sleeping-quarters hover updates the task preview.
- All six SVG regions open their corresponding dashboards by click.
- Keyboard focus updates the preview; Tab reaches the next building; Enter and Space navigate.
- Plotly renders an actual interactive chart in the browser.
- A symptom observation saves through the real form; checkbox completion updates homepage progress.
- The JSON export initiates a real file download.
- A real sample upload changes the data-source indicator; an invalid second upload reports the error and keeps the valid data loaded.
- Touching the greenhouse shows its preview; the readable mobile building controls and Open dashboard button work.
- No uncaught JavaScript errors or Streamlit exceptions occurred in the desktop flow.

Desktop, dashboard and mobile screenshots were inspected. Visual review identified and corrected a small-label issue on mobile, header overlap, and a map-label collision. Mobile has six readable, labelled controls in addition to the SVG and sidebar.

### Repeat the browser checks (optional)

In one terminal, from the repository root with `.venv` active:

```bash
python -m streamlit run app.py
```

In another terminal, activate the same project environment, then:

```bash
# Test tooling only; not required to run the app
python -m pip install playwright==1.65.2
python -m playwright install chromium
python tests/browser_smoke.py --url http://127.0.0.1:8501
```

To use an existing browser instead of downloading Chromium, pass `--browser` followed by its executable path. For example, on a Mac with Chrome:

```bash
python tests/browser_smoke.py --browser "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

`--screenshots /path/to/a/local/output-folder` saves desktop, dashboard and mobile screenshots. Keep test output outside the source tree.

## Verification limits

- Windows commands are documented but were not executed on a Windows machine.
- Mobile is Chrome device emulation, not a physical iOS/Android device. Safari/Firefox and a screen reader were not tested.
- No Streamlit Community Cloud account was connected or deployment performed. The source includes the documented deployment inputs; actual hosting still needs the team to push and deploy it.
- There is no wearable/API provider to test. Adapter tests use a local fixture, with no fabricated live connection.
- Session storage is intentionally ephemeral; there is no database or JSON restore feature to test.
