# Hosting Astrocyte

The app requires a Python server. It cannot be published as a static HTML site or through GitHub Pages.

## Streamlit Community Cloud

1. Push the reviewed source to the GitHub repository and make the repository public if that is your release plan.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), create an app from the repository.
3. Select the release branch (normally `main`) and entrypoint **`app.py`**.
4. In **Advanced settings**, select **Python 3.12**. No secrets are needed for the bundled demo.
5. Deploy. After installation, test the dashboard, every crew profile, map task guides, both profile popups, and task completion.

The root `requirements.txt` declares the pinned Python packages. `.streamlit/config.toml` contains the shared theme; `.python-version` records the local development version but does not replace the host's Python selector. No OS packages, build step, API service or external database are required.

References: [file organization](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization), [dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies), [deployment settings](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Other Python hosts

Install `requirements.txt` in a Python 3.12 environment, then use:

```bash
python -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
```

Set the port to the host's assigned port if it differs. The reverse proxy must support WebSockets and HTTPS. The server's readiness endpoint is `/_stcore/health` on that port. Keep Streamlit's default CORS/XSRF protections enabled.

Include `data/`, `frontend/` and `.streamlit/config.toml` in the deployment. No files from `.venv` or a developer's Downloads folder are needed. Google Fonts and FlagCDN are external browser resources; fallback fonts work if unavailable.

## Release checks

- Run `python -m unittest discover -s tests -v` and `git diff --check`.
- Review the staged diff and ensure there are no secrets or personal medical records.
- Confirm permission/provenance for the supplied logo and environmental CSV as described in [third-party notices](../THIRD_PARTY_NOTICES.md).
- Verify the public app's wording does not imply live sensors, clinical validation or persistent test logging.
- Recheck the main browser flows after deployment, including a new browser session. Session-local task state resets in a new session or after server restart.

No deployment is performed by the test workflow or by these instructions.
