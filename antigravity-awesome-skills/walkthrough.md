# Maintenance Walkthrough - 2026-03-18

- Fixed issue `#344` by correcting `.claude-plugin/marketplace.json` so the marketplace plugin entry uses `source: "./"` instead of `"."`, matching Claude Code's relative-path schema requirement for marketplace entries.
- Added `tools/scripts/tests/claude_plugin_marketplace.test.js` and wired it into the local test suite so invalid marketplace `source` paths fail fast in CI/maintainer verification.
- Merged PRs `#333`, `#336`, `#338`, `#343`, `#340`, `#334`, and `#345` via GitHub squash merge after maintainer refresh of forked workflows and PR metadata.
- Closed PR `#337` and PR `#342` as superseded by `#338`, then closed issue `#339` manually after confirming the accepted fix path; issue `#335` auto-closed from the merged PR body.
- Closed issue `#344` with a follow-up comment after shipping the plugin marketplace fix on `main`, and left PR `#341` open with a blocking review comment because the submitted skill content is corrupted even though CI is green.
- Documented a new maintainer edge case in `.github/MAINTENANCE.md`: forked runs in `action_required`, `pr-policy` failures caused by stale PR bodies, the REST API fallback when `gh pr edit` fails with the Projects Classic GraphQL error, and the need to `close`/`reopen` a PR when a plain rerun does not pick up updated metadata.
- Refreshed the release-facing docs for `8.2.0` across `README.md`, `docs/users/getting-started.md`, `docs/users/walkthrough.md`, and `CHANGELOG.md`.
- Published release `v8.2.0` on `main` with:
  - `npm run release:preflight`
  - `npm run security:docs`
  - `npm run release:prepare -- 8.2.0`
  - `npm run release:publish -- 8.2.0`

# Maintenance Walkthrough - 2026-03-17

- Synced `main` after the six merged community PRs and re-verified all forked PR workflows through GitHub before final release prep.
- Reopened/approved forked GitHub Actions runs where needed, normalized missing PR quality checklists, and merged PRs `#331`, `#330`, `#326`, `#324`, `#325`, and `#329` with GitHub squash merge.
- Patched `skills/vibers-code-review/SKILL.md` on the contributor branch for PR `#325` so the skill had valid YAML frontmatter, a `When to Use` section, and explicit limitations; reran CI and merged after green checks.
- Closed issue `#327` with a release comment pointing to `#331`, and closed issue `#328` as a duplicate of `#269` with links to the README recovery guidance and `docs/users/windows-truncation-recovery.md`.
- Updated release-facing docs before cutting `v8.1.0`:
  - `README.md`
  - `docs/users/getting-started.md`
  - `CHANGELOG.md`
  - `walkthrough.md`
- Refreshed the README contributor acknowledgements to include the latest merged contributors from the maintenance batch.
- Release workflow to run for `8.1.0`:
  - `npm run release:preflight`
  - `npm run security:docs`
  - `npm run release:prepare -- 8.1.0`
  - `npm run release:publish -- 8.1.0`

# Maintenance Walkthrough - 2026-03-12

- Merged PRs `#277`, `#272`, `#275`, `#278`, and `#271` via GitHub squash merge after bringing contributor branches into a mergeable state and refreshing PR bodies against the quality checklist in `.github/MAINTENANCE.md`.
- Verified PR `#271` locally with `npm run validate:references` and `npm run test` before merge; confirmed `#269` auto-closed from the merged PR body.
- Added a user-facing Windows truncation recovery guide at `docs/users/windows-truncation-recovery.md`, linked it from `README.md`, `docs/users/faq.md`, `docs/users/getting-started.md`, and `docs/integrations/jetski-cortex.md`, and credited the workflow to issue `#274`.
- Updated `skills/metasploit-framework/SKILL.md` to remove the remote installer flow, require an existing Metasploit installation, and add the required offensive-skill warning.
- Refreshed `README.md` to remove stale `7.2.0` / `7.4.0` onboarding copy, align the star badge with the current milestone, and fix the TOC link for `## Contributing`.
- Normalized the active English docs (`README.md`, user guides, Kiro guide, and evergreen maintainer docs) to the current `7.6.0` / `1,250+ skills` state and removed emoji from H2 headers where maintenance rules require clean anchors.
- Ran the required maintenance validations after the direct fixes:
  - `npm run validate`
  - `npm run validate:references`
  - `npm run chain`
  - `npm run catalog`
- Final release prep, issue closure comments, and verification were completed on `main`.

# Maintenance Walkthrough - 2026-03-13

- Fixed `tools/scripts/update_readme.py` so normal `npm run readme` runs preserve the existing `registry-sync` star/timestamp values instead of rewriting them on every execution, which was causing non-deterministic PR drift failures in CI.
- Updated `tools/scripts/sync_repo_metadata.py` to expose the same explicit `--refresh-volatile` behavior for live star/timestamp refreshes, keeping release/metadata refresh flows available without destabilizing contributor PR checks.
- Updated `.github/workflows/ci.yml` so generated registry drift is informational on pull requests but still strict on `main`, with auto-sync remaining the canonical path for shared artifacts after merge.
- Updated `.github/MAINTENANCE.md`, `docs/maintainers/ci-drift-fix.md`, and `docs/maintainers/merging-prs.md` to document the lower-friction merge flow: validate source changes on PRs, keep `main` for generated conflicts, and let `main` auto-sync the final artifact set.
- Verified the fix with:
  - `python3 tools/scripts/update_readme.py --dry-run`
  - `python3 tools/scripts/sync_repo_metadata.py --dry-run`
  - `npm run readme`
  - `npm run validate:references`
- Added `tools/config/generated-files.json` as the single contract for derived registry artifacts so CI, maintainer scripts, and docs share the same file list.
- Added scripted workflow entrypoints: `npm run pr:preflight`, `npm run release:preflight`, `npm run release:prepare -- X.Y.Z`, and `npm run release:publish -- X.Y.Z`.
- Split PR CI into `pr-policy`, `source-validation`, and `artifact-preview` so PRs stay source-only, policy failures are explicit, and generated drift is previewed separately from source validation.
- Updated `CONTRIBUTING.md` and `.github/PULL_REQUEST_TEMPLATE.md` so contributors are told not to commit derived files and to enable `Allow edits from maintainers`.

# Maintenance Walkthrough - 2026-03-14

- Added root Claude Code plugin marketplace support via `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, exposing the repository as a single plugin entry that points at the existing `skills/` tree.
- Updated the user onboarding trinity (`README.md`, `docs/users/getting-started.md`, `docs/users/faq.md`) so Claude Code users can install via `/plugin marketplace add sickn33/antigravity-awesome-skills` in addition to the existing `npx` installer flow.
- Merged PRs `#302`, `#301`, `#299`, `#297`, `#296`, `#287`, `#298`, and `#293` via GitHub squash merge after maintainer preflight, including a maintained follow-up commit on the contributor branch for `#298` and a maintainer conflict-resolution refresh on `#293`.
- Verified the issue-driven fixes locally before merge:
  - `#301`: `python3 -m py_compile skills/notebooklm/scripts/browser_utils.py`
  - `#299`: `node -c tools/bin/install.js`
- Verified the skill/docs PRs locally before merge:
  - `#297`, `#296`, `#287`, `#298`: `npm run validate`
  - `#293`, `#298`: `npm run validate:references`
- Closed issues `#288`, `#300`, `#286`, and `#281` from the merged fixes and release notes flow; documented `#294` as a release follow-up because the support already exists in the current catalog.
- Removed stale Windows `core.symlinks=true` / Developer Mode guidance from the user docs after the `#299` installer fix, keeping the Windows path on the standard clone/install flow.
- Ran the post-merge maintainer sync on `main`:
  - `npm run chain`
  - `npm run catalog`
- Refreshed `CHANGELOG.md`, `README.md`, `docs/users/getting-started.md`, `docs/users/faq.md`, and the contributor acknowledgements to prepare the single `7.8.0` release cut.
