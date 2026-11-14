# Working on the blank template together

Each teammate clones the same repository, creates their own `.venv` inside it, and follows the setup commands in `README.md`. Never commit a virtual environment or credentials.

## Keep edits independent

Each page has its own file under `views/`. Divide those files between teammates and agree before editing a file someone else owns. Person 4 can integrate changes to `app.py`, `components/sidebar.py` and `models/areas.py`; Person 2 can coordinate dependencies in `requirements.txt`.

Use `frontend/` for styling/map assets, `components/` for reusable widgets, `services/` for data/storage logic and `models/` for shared definitions. These are workspaces, not implemented health features.

## Branch workflow

Start from a clean, updated main branch:

```bash
git switch main
git pull --ff-only
git switch -c feature/your-task
```

Edit your assigned files, then:

```bash
python -m unittest discover -s tests -v
git status
git add path/to/your/changed_files
git commit -m "Describe the change"
git push -u origin feature/your-task
```

Replace example paths and branch names with your own. Open a pull request into `main` and ask a teammate to review it. Keep each request focused on one change. When you add real page content, update that page's expectations in `tests/test_app.py` and add meaningful tests for the new behaviour.

After a merge, switch to `main`, run `git pull --ff-only`, and reinstall `requirements.txt` if dependencies changed. Commit unfinished work on your feature branch before switching away.

To bring main's changes into an existing feature branch:

```bash
git fetch origin
git switch feature/your-task
git merge origin/main
```

## Merge conflicts

Run `git status`, coordinate with the other file owner, and combine both intended changes in VS Code's merge editor. Remove conflict markers, run the tests, stage the resolved files and commit the merge. To cancel an in-progress merge, use `git merge --abort`. Do not force-push someone else's branch or use a hard reset to hide a conflict.

`.gitignore` excludes environments, personal editor settings, caches, secrets and local runtime data. Review `git status` before committing; do not add private health data or exported personal notes.
