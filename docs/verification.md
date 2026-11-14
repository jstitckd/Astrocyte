# Seven-zone habitat map verification

Run from the repository root with the project environment:

```bash
python -m unittest discover -s tests -v
```

All **six integration tests pass** on macOS with Python 3.12 and Streamlit AppTest:

1. New habitat destinations and older health/data routes render without exceptions; habitat pages stay title-only.
2. The existing Alex crew sidebar route and return to Base overview still work.
3. All seven map messages open the correct page; returning home does not replay the last activation.
4. Unknown, malformed and obsolete map messages leave the homepage open.
5. Exactly seven SVG regions match the Python registry, with focusable button roles and no duplicate IDs.
6. An unknown saved page ID returns to the homepage.

## Real-browser verification

Headless Chrome checks passed at desktop 1512 × 1100 and touch-enabled mobile emulation 390 × 844:

- All seven SVG regions show the correct hover preview, description and three facility tags.
- Every region opens its corresponding page and returns home correctly.
- All seven labelled guide buttons navigate on desktop.
- Tab moves between buildings; Enter and Space activate them.
- The existing crew page still opens from the sidebar.
- The mobile layout has seven readable guide controls and no component horizontal overflow.
- Mobile guide taps preview a space; Open space navigates. Direct building taps also work.
- No uncaught JavaScript errors or Streamlit exceptions occurred.

Desktop and mobile screenshots were inspected. Visual review corrected the ground beneath the front solar array and increased label text size. `docs/habitat-map-preview.png` records the final desktop overview.

## Scope and limits

The SVG is a concept illustration, not a verified engineering plan. The map generates no live system readings, health scores or operational statuses. The seven habitat destination pages are blank workspaces; the team's existing crew page is preserved.

Windows, physical mobile devices, Safari/Firefox, screen readers and Streamlit Community Cloud were not tested for this revision. No deployment, commit or GitHub push was performed as part of this change.
