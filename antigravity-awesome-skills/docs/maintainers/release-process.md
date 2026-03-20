# Release Process

This is the maintainer playbook for cutting a repository release. Historical release notes belong in [`CHANGELOG.md`](../../CHANGELOG.md); this file documents the repeatable process.

## Preconditions

- The tracked working tree is clean.
- You are on `main`.
- `CHANGELOG.md` already contains the release section you intend to publish.
- README counts, badges, and acknowledgements are up to date.

## Release Checklist

1. Run the scripted preflight:

```bash
npm run release:preflight
```

2. Mandatory documentation hardening (repo-wide SKILL.md security scan):

```bash
npm run security:docs
```

This is required so every release validates repo-wide risky command patterns and inline token-like examples before publishing.

3. Optional hardening pass:

```bash
npm run validate:strict
```

Use this as a diagnostic signal. It is useful for spotting legacy quality debt, but it is not yet the release blocker for the whole repository.

4. Update release-facing docs:

- Add the release entry to [`CHANGELOG.md`](../../CHANGELOG.md).
- Confirm `README.md` reflects the current version and generated counts.
- Confirm Credits & Sources, contributors, and support links are still correct.
- If PR or CI workflow behavior changed during the cycle, confirm maintainer and contributor docs mention the active checks (for example the `skill-review` workflow for `SKILL.md` pull requests).

5. Prepare the release commit and tag locally:

```bash
npm run release:prepare -- X.Y.Z
```

This command:

- checks `CHANGELOG.md` for `X.Y.Z`
- aligns `package.json` / `package-lock.json`
- runs the full release suite
- refreshes release metadata in `README.md`
- stages canonical release files
- creates `chore: release vX.Y.Z`
- creates the local tag `vX.Y.Z`

6. Publish the GitHub release:

```bash
npm run release:publish -- X.Y.Z
```

This command pushes `main`, pushes `vX.Y.Z`, and creates the GitHub release object from the matching `CHANGELOG.md` section.

7. Publish to npm if needed:

```bash
npm publish
```

Normally this still happens via the existing GitHub release workflow after the GitHub release is published.

## Rollback Notes

- If the release tag is wrong, delete the tag locally and remotely before republishing.
- If generated files drift after tagging, cut a follow-up patch release instead of mutating a published tag.
- If npm publish fails after tagging, fix the issue, bump the version, and publish a new release instead of reusing the same version.
