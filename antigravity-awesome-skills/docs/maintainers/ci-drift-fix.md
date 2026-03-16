# CI Drift Fix Guide

**Problem**: The failing job is caused by uncommitted changes detected in `README.md`, `skills_index.json`, or catalog files after the update scripts run.

**Error**:

```
❌ Detected uncommitted changes produced by registry/readme/catalog scripts.
```

**Cause**:
Scripts like `tools/scripts/generate_index.py`, `tools/scripts/update_readme.py`, and `tools/scripts/build-catalog.js` modify `README.md`, `skills_index.json`, `data/catalog.json`, `data/bundles.json`, `data/aliases.json`, and `CATALOG.md`. The workflow expects these files to have no changes after the scripts run. Any differences mean the committed repo is out-of-sync with what the generation scripts produce.

## Pull Requests vs Main

- **Pull requests**: PRs are now **source-only**. Contributors should not commit derived registry artifacts (`CATALOG.md`, `skills_index.json`, `data/*.json`). CI blocks those direct edits and reports generated drift as an informational preview only.
- **`main` pushes**: drift is still strict. `main` must end the workflow clean after the auto-sync step.

## How to Fix on `main`

1. Run the **FULL Validation Chain** locally:

   ```bash
   npm run chain
   npm run catalog
   ```

2. Check for changes:

   ```bash
   git status
   git diff
   ```

3. Commit and push any updates:
   ```bash
   git add README.md skills_index.json data/skills_index.json data/catalog.json data/bundles.json data/aliases.json CATALOG.md
   git commit -m "chore: sync generated registry files"
   git push
   ```

## Maintainer guidance for PRs

- Validate the source change, not the absence of committed generated artifacts.
- If a contributor PR includes direct edits to `CATALOG.md`, `skills_index.json`, or `data/*.json`, ask them to drop those files from the PR or remove them while refreshing the branch.
- If merge conflicts touch generated registry files, keep `main`'s version for those files and let `main` auto-sync the final generated artifact set after merge.

**Summary**:
Use generator drift as a hard failure only on `main`. On PRs, the contract is simpler: source-only changes are reviewed, generated output is previewed, and `main` produces the final canonical artifact set.
