# Finding taxonomy

A finding is evidence that deserves investigation. It is not automatically a defect.

Before mutating code, establish:

**Observed pattern, then actual consequence, then owning layer, then repository evidence, then appropriate correction.**

A scanner match, generic style preference, complexity number, or resemblance to common AI-generated code is insufficient by itself.

## 1. Repository conformity

Look for changes that introduce a second way to solve a problem the repository already solves coherently.

Examples include parallel:

- validation systems;
- error models;
- persistence access paths;
- logging conventions;
- configuration mechanisms;
- helper ecosystems;
- domain models.

Diagnosis requires comparing semantics and ownership, not just names.

A different implementation is acceptable when its domain, lifecycle, boundary, or invariants genuinely differ.

## 2. Domain semantic erosion

Look for lost or weakened domain meaning.

Signals include generic names at domain-significant scope, loosely typed business states, business rules hidden inside technical transformations, or domain concepts flattened into generic payloads.

Restore terminology only from repository or task evidence.

Do not invent more sophisticated-sounding vocabulary.

Short generic locals in tiny scopes are not automatically problematic.

## 3. Architectural fragmentation

Look for:

- responsibilities placed outside their natural owner;
- feature logic split across unnecessary technical layers;
- accidental service/factory/adapter chains;
- oversized orchestration functions;
- abstractions with no present policy or boundary value;
- local solutions that bypass established architecture.

Do not judge architecture from file count alone.

A thin abstraction may legitimately encode dependency direction, ownership, compatibility, policy, or test boundaries.

## 4. Reinvention and duplication

Distinguish:

**same syntax**

from

**same concept**.

Code should normally be consolidated only when implementations share:

- ownership;
- invariants;
- semantic purpose;
- expected reasons to change.

Two similar blocks in different domains may intentionally remain separate.

## 5. Error semantics

Look for:

- swallowed errors;
- fake success;
- universal empty fallbacks;
- lost context;
- logging at multiple ownership layers;
- retry at the wrong layer;
- infrastructure failure converted into misleading domain data.

Determine the error owner before changing propagation.

“Fail loudly” is not a universal rule.

## 6. Type and schema integrity

Investigate:

- unchecked external data;
- unsafe type suppression;
- unexplained assertions;
- loose object/dict structures crossing domain boundaries;
- mismatch between runtime validation and static types;
- duplicated incompatible schemas.

Escape hatches are findings, not automatic defects.

A local assertion at a known third-party boundary may be intentional.

## 7. Testing integrity

Look for:

- implementation logic copied into expected values;
- mocks that replace the behavior being tested;
- tests coupled to private implementation unnecessarily;
- assertions weakened to accommodate a change;
- regression cases removed;
- meaningless tests created for apparent coverage.

A passing test is useful evidence only to the extent that the test independently constrains behavior.

## 8. Security and reliability

Inspect relevant changes for:

- missing authorization;
- insecure defaults;
- lost validation;
- unbounded retry;
- missing timeout;
- incorrect cleanup;
- broken idempotency;
- partial-failure handling;
- unsafe concurrency;
- transaction leaks;
- secrets exposed to logs.

Treat these areas as high semantic risk.

## 9. Repository prose and communication integrity

Inspect comments, docstrings, test descriptions, errors, logs, command output, and user-facing strings according to their distinct roles.

Look for:

- narration that restates syntax or execution order;
- inflated or generic claims without a concrete invariant;
- documentation that repeats names and types but adds no contract;
- stale prose that contradicts behavior;
- domain language flattened into generic wording;
- valuable rationale buried inside lengthy explanation;
- observable strings reworded as if they were internal comments.

Prose that resembles common AI output is a finding, not proof that it is wrong. Resolve the repository's local prose conventions, then decide whether to delete, preserve, tighten, correct, or report it.

Do not use phrase blacklists, comment quotas, or AI-detector scores as mutation authority. Read [repository-native prose](repository-prose.md) when prose is material to the cleanup.

## 10. Operational quality

Look for:

- temporary debug output;
- incorrect log ownership;
- missing structured context;
- accidental config drift;
- speculative environment flags;
- divergent metrics/tracing conventions;
- output changes that consumers may observe.

Remember that output can be a contract.

## 11. Change discipline

Look for:

- unrelated cleanup;
- mass formatting;
- opportunistic renaming;
- dependency churn;
- broad modernization;
- multiple unrelated architectural changes in one diff;
- generated artifacts edited outside normal workflow.

A technically “better” change can still be a worse patch if it becomes harder to review, revert, or reason about.
