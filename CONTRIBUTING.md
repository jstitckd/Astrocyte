# Working together

Each teammate clones the **same repository**, then creates their own `.venv` **inside their clone**. Never send your `.venv` to another person. Follow the exact macOS or Windows commands in [README.md](README.md) and open `Astrocyte.code-workspace` in VS Code.

## Before editing

1. Tell the team which area you are working on. Follow the owner table in the README; coordinate before changing another owner's files.
2. Read [docs/interfaces.md](docs/interfaces.md). Agree on changes to IDs, arguments or data schemas before implementing them.
3. From a clean `main`, get the team's changes and create a branch:

```bash
git switch main
git pull --ff-only
git switch -c feature/your-short-description
```

Use names such as `feature/map-labels`, `feature/csv-provider`, or `feature/nutrition-form`. Person 3 integrates the small entry point and shared area registry; announce changes there to avoid simultaneous edits.

## Work, test and share

```bash
# Run from the Astrocyte repository folder, with .venv activated
python -m streamlit run app.py
# Stop with Ctrl+C, then:
python -m unittest discover -s tests -v
git status
git add path/to/the/files/you/changed
git commit -m "Describe the user-visible change"
git push -u origin feature/your-short-description
```

Replace the example paths with your actual files. Open a pull request on GitHub into `main`. Explain what changed and how you checked it; ask a teammate to review. Keep one feature per pull request. Include screenshots for map/style changes and tests for data/workflow changes.

Source, dependency files, safe theme configuration and synthetic data belong in Git. `.gitignore` excludes `.venv`, personal editor settings, caches, secrets and local runtime databases. Double-check `git status` before committing; do not include real health records, API keys or exported private notes.

## Bring in teammates' changes

After a pull request is merged:

```bash
git switch main
git pull --ff-only
python -m pip install -r requirements.txt
```

If you have uncommitted edits, commit them on your feature branch first, or save them with `git stash push -m "work in progress"`. To update an existing feature branch with current `main` without rewriting its shared history:

```bash
git fetch origin
git switch feature/your-short-description
git merge origin/main
```

Do not force-push teammates' branches. If `git pull --ff-only` fails, stop and inspect `git status` and `git log --oneline --graph --all`; coordinate before combining divergent work.

## If a merge conflicts

Run `git status` to see the conflicted files. Ask the owner of the other change what should survive. In VS Code's merge editor, combine the intended changes; remove `<<<<<<<`, `=======`, and `>>>>>>>` markers. Do not blindly choose one whole file. Then:

```bash
python -m unittest discover -s tests -v
git add path/to/resolved_file.py
git commit
git push
```

To cancel an in-progress merge and return to the pre-merge state, use `git merge --abort`. Do not delete files or use a hard reset to make a conflict disappear. Ask a teammate when uncertain.
