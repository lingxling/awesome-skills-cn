# Repo coherence and correctness audit

This document summarizes the repository coherence audit performed after the `apps/` + `tools/` + layered `docs/` refactor.

## Scope

- Conteggi e numeri (README, package.json, CATALOG)
- Validazione skill (frontmatter, risk, "When to Use", link)
- Riferimenti incrociati (workflows.json, bundles.json, `docs/users/bundles.md`)
- Documentazione (`docs/contributors/quality-bar.md`, `docs/contributors/skill-anatomy.md`, security/licenses)
- Script e build (validate, index, readme, catalog, test)
- Note su data/ e test YAML

## Outcomes

### 1. Conteggi

- `README.md`, `package.json`, and generated artifacts are aligned to the current collection size (`1,204+` skills).
- `npm run sync:all` and `npm run catalog` are the canonical commands for keeping counts and generated files synchronized.

### 2. Validazione skill

- `npm run validate` is the operational contributor gate.
- `npm run validate:strict` is currently a diagnostic hardening pass: it still surfaces repository-wide legacy metadata/content gaps across many older skills.
- The validator accepts `risk: unknown` for legacy/unclassified skills while still preferring concrete risk values for new skills.

### 3. Riferimenti incrociati

- Added `tools/scripts/validate_references.py` (also exposed as `npm run validate:references`), which verifies:
  - ogni `recommendedSkills` in data/workflows.json esiste in skills/;
  - ogni `relatedBundles` esiste in data/bundles.json;
  - ogni slug in data/bundles.json (skills list) esiste in skills/;
  - every skill link in `docs/users/bundles.md` points to an existing skill.
- Execution: `npm run validate:references`. Result: all references valid.

### 4. Documentazione

- Canonical contributor docs now live under `docs/contributors/`.
- Canonical maintainer docs now live under `docs/maintainers/`.
- README, security docs, licenses, and internal markdown links were rechecked after the refactor.

### 5. Script e build

- `npm run test` and `npm run app:build` complete successfully on the refactored layout.
- `validate_skills_headings.test.js` acts as a lightweight regression/smoke test, not as the source of truth for full metadata compliance.
- The maintainer docs now need to stay aligned with the root `package.json` and the refactored `tools/scripts/*` paths.

### 6. Deliverable

- Counts aligned to the current generated registry.
- Reference validation wired to the refactored paths.
- User and maintainer docs checked for path drift after the layout change.
- Follow-up still open: repository-wide cleanup required to make `validate:strict` fully green.

## Comandi utili

```bash
npm run validate          # validazione skill (soft)
npm run validate:strict   # hardening / diagnostic pass
npm run validate:references  # workflow, bundle, and docs/users/bundles.md references
npm run build             # chain + catalog
npm test                  # suite test
```

## Issue aperte / follow-up

- Gradual cleanup of legacy skills so `npm run validate:strict` can become a hard CI gate in the future.
- Keep translated docs aligned in a separate pass after the canonical English docs are stable.
