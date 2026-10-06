# Testing integrity

Tests are evidence.

They are not automatically truth.

The audit must consider both:

**implementation quality**

and

**test quality**.

## Evidence confidence

### High confidence

Examples:

- contract tests;
- integration tests;
- independent expected values;
- observable end-to-end behavior;
- regression tests tied to an externally visible failure.

### Medium confidence

Examples:

- meaningful unit tests around public behavior;
- isolated business-rule tests with independent fixtures.

### Low confidence

Examples:

- expectations copied from implementation logic;
- excessive implementation mocking;
- tests of private structure;
- snapshots with little semantic meaning;
- tests asserting only that mocks were called.

Higher semantic risk requires stronger evidence.

If R3/R4 code has weak test evidence, reduce refactor aggressiveness.

## Test-slop patterns

### Tautological expectations

Bad pattern:

implementation computes X using formula F; test independently reproduces formula F and compares both.

The test may repeat the same mistake.

Prefer independent business examples or externally defined expected outcomes.

### Mock theatre

Mocking is not inherently bad.

The problem occurs when nearly every dependency is replaced and the test validates only the configured mocks rather than meaningful behavior.

Mock external or expensive boundaries when appropriate.

Do not mock away the behavior being audited.

### Test weakening

Never make a refactor pass by:

- deleting a regression case;
- changing a precise assertion into a vague one;
- disabling a test;
- expanding tolerances without domain justification.

If behavior intentionally changes, update tests because the contract changed, and report that behavioral change explicitly.

### Implementation coupling

Refactoring internals should not require widespread test rewrites when public behavior is unchanged unless repository conventions intentionally test internal units.

Large test churn during a behavior-preserving refactor is a warning sign.

### Test prose

Test names should describe meaningful behavior using the repository's vocabulary. Do not lengthen them into narrative specifications merely to appear thorough, and do not shorten them until the behavior under test becomes ambiguous.

Assertion messages, expected errors, snapshots, and golden output may constrain observable wording. Do not update them solely to accommodate stylistic rewording. If the contract intentionally changes, report it and retain independent behavioral evidence.

## Verification strategy

Prefer the smallest validation set that meaningfully constrains the change, then expand when risk requires it.

Mechanical cleanup may need type/lint/unit checks.

Structural changes may require focused unit and integration checks.

Semantic and critical-boundary changes may require contract, integration, security, or end-to-end verification.

Do not claim verification beyond what was actually run.
