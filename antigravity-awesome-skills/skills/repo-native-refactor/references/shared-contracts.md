# Shared contracts

These rules apply to repository development and review.

## 1. Strict contract adherence (canonical wording)

Preserve documented or demonstrably consumed public contracts across public interfaces,
exported parameters, module constants, return types, errors, and serialization.

- A requested behavior change may authorize a contract change only when that consequence
  is clear from the task or from an authorized evolution. Then update affected callers,
  tests, and living documentation within scope.
- Otherwise preserve exact declared types. For example, never substitute or wrap an exposed
  primitive `str` path contract with `pathlib.Path` or custom wrapper objects merely for
  internal convenience or preference.
- Internal intermediate representations may use appropriate helpers, provided all exposed
  public contracts and types remain exact.

## 2. Evidence hierarchy (canonical order)

Use to guide investigation, not to auto-resolve material contradictions:

1. User requirements and explicitly authorized scope.
2. Documented architecture and repository guidelines.
3. Observable public contracts and persisted schemas.
4. Healthy sibling code within the same domain and runtime boundary.
5. Relevant tests, schemas, callers, and dependencies.
6. Dominant local conventions.
7. Language and runtime idioms.
8. Conservative, idiomatic defaults.

Never treat a temporary workaround, buggy sibling, or accidental pattern as precedent.
Never rewrite history or rubber-stamp code with stale notes. Reconcile before mutating
the affected contract.

## 3. Verification final-state rule (canonical)

- Record baseline failures as: (1) pre-existing outside scope, (2) in-scope to fix,
  (3) regressions from current changes, (4) environment errors.
- Verify the final code state. Never use pre-cleanup results to certify modified code.
- Never claim a check ran when it did not. Distinguish verified behavior,
  inspection-only conclusions, and unverified assumptions.

## 4. Shared judgment tests (canonical)

Two questions that both skills use when the text alone under-determines the answer.

A pattern counts as healthy precedent only if three things hold: code outside its original author consumes it, it does not contradict docs or contracts, and you would copy it into a new domain without apology. Popularity proves nothing; a workaround with tests and docs still fails. When two domains overlap, the owner is whoever owns the failure (who gets paged, who fixes the bug, whose reason to change fires first). Consolidate toward that owner, or leave both alone.
