# Template and starter-map verification

Run from the repository root using the project's environment:

```bash
python -m unittest discover -s tests -v
```

All four integration tests pass on macOS with Python 3.12 and Streamlit AppTest:

1. All eight sidebar routes render without errors; destination pages remain blank apart from their titles. No measurements, health charts, forms, uploads or exports are loaded.
2. All six map selections open their matching page, and returning home does not replay a previous selection.
3. Malformed or unknown map messages leave the homepage open.
4. An unknown saved page ID returns to the homepage.

Real-browser checks passed using headless Chrome at desktop 1512 × 1100 and touch-enabled mobile emulation 390 × 844:

- The homepage and SVG map load successfully.
- Hover changes the selected building's name and highlight colour.
- Every building opens the correct destination; returning home works.
- Tab reaches the next building, and Enter and Space open its page.
- Mobile labelled buttons preview the building and Open page navigates; direct SVG taps also open the matching page.
- No uncaught JavaScript errors or Streamlit exceptions occurred.

Desktop and mobile screenshots were inspected. The starter keeps all health dashboards and data services empty; only homepage map navigation has been added.

Windows, physical mobile devices, Safari/Firefox, screen readers and Streamlit Community Cloud were not tested for this revision. No deployment or GitHub push was performed. The existing project environment and workspace launcher are preserved.
