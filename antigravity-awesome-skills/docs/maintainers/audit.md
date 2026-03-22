# Repo coherence and correctness audit

This document summarizes the repository coherence audit performed after the `apps/` + `tools/` + layered `docs/` refactor.

## Scope

- Conteggi e numeri (README, package.json, CATALOG)
- Validazione skill (frontmatter, risk, "When to Use", link)
- Audit repo-wide per skill (conformance + baseline usability)
- Riferimenti incrociati (workflows.json, bundles.json, `docs/users/bundles.md`)
- Documentazione (`docs/contributors/quality-bar.md`, `docs/contributors/skill-anatomy.md`, security/licenses)
- Script e build (validate, index, readme, catalog, test)
- Note su data/ e test YAML

## Outcomes

### 1. Conteggi

- `README.md`, `package.json`, and generated artifacts are aligned to the current collection size.
- `npm run sync:all` and `npm run catalog` are the canonical commands for keeping counts and generated files synchronized.

### 2. Validazione skill

- `npm run validate` is the operational contributor gate.
- `npm run validate:strict` is currently a diagnostic hardening pass: it still surfaces repository-wide legacy metadata/content gaps across many older skills.
- The validator accepts `risk: unknown` for legacy/unclassified skills while still preferring concrete risk values for new skills.
- Repo-wide documentation risk guidance is now covered by `npm run security:docs`:
  - detects high-risk command guidance in `SKILL.md`,
  - requires explicit allowlists for deliberate command-delivery patterns,
  - and blocks token-like examples that look exploitable.

### 2b. Audit repo-wide per skill

- Added `tools/scripts/audit_skills.py` (also exposed as `npm run audit:skills`), which audits every `SKILL.md` and produces a per-skill status (`ok`, `warning`, `error`) with finding codes.
- The audit is intentionally broader than `validate` and covers:
  - truncated descriptions that likely map to issue `#365`,
  - missing examples and missing limitations sections,
  - overly long `SKILL.md` files that should probably be split into `references/`,
  - plus the existing structural/safety checks (frontmatter, risk, `When to Use`, offensive disclaimer, dangling links).
- Use `npm run audit:skills` for the maintainer view and `npm run audit:skills -- --json-out ... --markdown-out ...` when you want artifacts for triage or cleanup tracking.

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
npm run audit:skills      # audit completo per skill con finding codes e status
npm run validate:references  # workflow, bundle, and docs/users/bundles.md references
npm run security:docs       # documentation command-risk scan (required for security-sensitive guidance)
npm run build             # chain + catalog
npm test                  # suite test
```

## Issue aperte / follow-up

- Gradual cleanup of legacy skills so `npm run validate:strict` can become a hard CI gate in the future.
- Keep translated docs aligned in a separate pass after the canonical English docs are stable.
