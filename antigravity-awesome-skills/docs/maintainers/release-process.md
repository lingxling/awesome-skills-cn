# Release Process

This is the maintainer playbook for cutting a repository release. Historical release notes belong in [`CHANGELOG.md`](../../CHANGELOG.md); this file documents the repeatable process.

## Preconditions

- The working tree is clean, or you have explicitly isolated the release changes.
- `package.json` contains the version you intend to publish.
- Generated registry files are synchronized.
- README counts, badges, and acknowledgements are up to date.

## Release Checklist

1. Run the operational verification suite:

```bash
npm run validate
npm run validate:references
npm run sync:all
npm run test
npm run app:build
```

2. Optional hardening pass:

```bash
npm run validate:strict
```

Use this as a diagnostic signal. It is useful for spotting legacy quality debt, but it is not yet the release blocker for the whole repository.

3. Update release-facing docs:

- Add the release entry to [`CHANGELOG.md`](../../CHANGELOG.md).
- Confirm `README.md` reflects the current version and generated counts.
- Confirm Credits & Sources, contributors, and support links are still correct.

4. Create the release commit and tag:

```bash
git add README.md CHANGELOG.md CATALOG.md data/ skills_index.json package.json package-lock.json
git commit -m "chore: release vX.Y.Z"
git tag vX.Y.Z
```

5. Publish the GitHub release:

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file CHANGELOG.md
```

6. Publish to npm if needed:

```bash
npm publish
```

## Rollback Notes

- If the release tag is wrong, delete the tag locally and remotely before republishing.
- If generated files drift after tagging, cut a follow-up patch release instead of mutating a published tag.
- If npm publish fails after tagging, fix the issue, bump the version, and publish a new release instead of reusing the same version.
