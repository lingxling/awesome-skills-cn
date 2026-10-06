---
name: repo-foundation
description: "Implement features, fixes, modules, contract migrations, and resumed work while preserving user edits and authorized public contracts."
category: development
risk: critical
source: https://github.com/Natchannnn/repository-engineering-skills
source_repo: Natchannnn/repository-engineering-skills
source_type: community
date_added: "2026-09-30"
author: Natchannnn
tags: [repository-engineering, feature-development, contract-migration, continuity]
tools: [codex]
license: MIT
license_source: https://github.com/Natchannnn/repository-engineering-skills/blob/e55b378158d5134a77af3b8dace4a2a1b17e41e2/LICENSE
metadata:
  version: "0.3.0"
  license: "MIT"
---

# Repo foundation

## When to Use

- Use when the user asks to add a feature, fix a bug, or start a module in an existing project.
- Use when establishing the minimum foundation for a new repository or subsystem.
- Use when requirements authorize a schema, public-contract, ownership, or architecture migration.
- Use when resuming unfinished work or reconciling stale notes with repository evidence.

Build on a foundation that's just big enough, add features on top of it, and change the architecture only when requirements force it. Aim for the least total rework.

---

## Core principles

- **No universal dogma:** don't impose a layout, error pattern, or framework the project doesn't need. Plain standard library is fine.
- **Scope, baseline, and user work:**
  - Establish a clean baseline before mutating code: use the pre-existing revision/commit when Git exists; use a file inventory or snapshot when uninitialized or greenfield.
  - In a dirty workspace, protect pre-existing uncommitted user modifications. You may edit distinct parts of the same file as long as user work is preserved. Stop and ask only if there is an actual collision or ambiguous intent.
  - Never create commits or force Git initialization solely for handoff or tracking.
  - Reuse conventions only with healthy repository precedent. Don't treat accidental patterns or temporary workarounds as precedent, and don't expand into out-of-scope cleanup.
  - Don't push, publish, deploy, change branch protection, install system hooks, or buy anything unless the user asks.
- **Prose, naming, and restraint:**
  - Names reflect business domain concepts and ownership.
  - Add comments only for information code cannot express: grounded rationale, non-obvious invariants, units, rounding, ordering, protocol quirks, or compatibility.
  - Do not narrate syntax; do not invent tickets, incidents, owners, or production histories.
  - Treat error and CLI text as contract surface: check callers and parsers before rewording.
  - Never invent ticket, PR, or incident references. An inaccessible or unverified reference is not evidence of fabrication. Preserve existing references unless repository evidence establishes that they are incorrect or obsolete; report material uncertainty instead of deleting them.
  - Do not strip valuable comments merely for cosmetic brevity; do not enforce arbitrary comment ratios.
  - Do not add abstractions, wrappers, or factory layers without concrete ownership, contract, or test seam needs.
- **Preserve consumed public contracts** as defined in `references/shared-contracts.md` §1: keep documented types, values, errors, and serialization. Change a contract only when the task clearly authorizes it, then update callers, tests, and docs in scope.
- **Verification rigor & proportionate testing:**
  - Record baseline failures and distinguish: (1) pre-existing failures outside scope, (2) in-scope failures to fix, (3) regressions from current changes, and (4) environment errors.
  - Verify the final code state; never use pre-cleanup test results to certify modified code.
  - Add or update persistent tests when a change introduces behavior, fixes a defect, alters a contract, or exposes a meaningful coverage gap. Prefer the repository's existing test framework and structure. Do not add tests solely for file-count or coverage optics. For documentation-only or mechanically verified changes, use the relevant lightweight checks and explain any material verification gap.
  - Check every requirement before you say you're done. Say what you verified, what you only read, and what you assumed. A command that exits 0 doesn't count if the file it should make isn't there.
- **Failure invariants & state preservation:** if an operation can fail halfway, decide what must stay untouched. Validate inputs and ownership first, build the replacement on the side, keep the old state until the new one is ready, and test the failure boundary.

---

## Mode selection

| Mode | Trigger | Core Actions | Exit Criteria |
|---|---|---|---|
| **Bootstrap** | New repository from scratch or an area lacking minimal foundation (no build/test/run commands, conventions, or boundaries). | Elicit critical constraints, choose just-enough design, set up minimal tooling/checks, implement and verify the first representative slice. Read [bootstrap](references/bootstrap.md). | Representative slice works and is verified; run/build commands are documented; repo is stable for subsequent work. |
| **Continue** | Adding a feature, bugfix, or improvement on an existing, fitting foundation. | Determine owning domain and boundary, implement changes, run proportionate checks, and review diff. Executable directly from core. | Task requirements are met; diff is reviewed; intentional contract changes are verified (or existing contracts preserved); remaining limitations are stated. |
| **Evolve** | New requirements alter core contracts, ownership, boundaries, or architecture; or adopting a repo with conflicting conventions. | Assess blast radius, execute controlled migration, update evidence, tests, and documentation. Read [evolution](references/evolution.md). | Transition is verified; new contracts are operational; instructions and documentation align with code. |

Adopting an existing repository begins with mode selection; do not default to re-bootstrapping. If the repository already has working instructions, tooling, and conventions, reuse them. If a specific subsystem lacks a foundation, establish only what that subsystem requires.

---

## Continue workflow (Core)

Routine feature work runs straight from the mode above plus core principles, no extra reference needed:

### 1. Scope and baseline
Confirm the user's objective, observable consequences, affected boundaries, baseline revision/inventory, and any uncommitted user changes to preserve.

### 2. Implement just enough
- **Assumptions vs. product decisions:** choose conventional, reversible defaults (directory layout, helper naming, standard library choices) on your own. Bundle product and architectural decisions (external dependencies, data schema changes, new auth schemes) into one question before breaking anything.
- **Intentional contract changes** occur when a task explicitly requires changing a contract, so verify that callers and tests reflect the new contract rather than forcing deprecated behavior.

### 3. Verify proportionately
- **Lightweight path (low risk):** routine bug fixes and localized edits inside established boundaries. Keep scope tight and run relevant mechanical checks (syntax, linter, affected unit tests). Skip automatic secondary review passes unless concrete unresolved concerns warrant one; an explicit review request still applies.
- **High-risk changes:** a single line touching authorization, permissions, data migrations, cryptography, persistence lifecycles, or concurrency can do serious damage. Read [verification](references/verification.md) before designing checks.

### 4. Continuity and state
- **Implementation vs. requirements:** existing code shows current behavior. That is not proof of meeting requirements, and passing tests don't guarantee completeness if acceptance was never tested.
- **Reconciliation:** use the evidence hierarchy to guide investigation, not to settle contradictions for you. If requirements, docs, callers, and tests disagree, reconcile them before changing the contract. If notes and code disagree, check requirements and tests; don't edit the notes to match the code.
- **Tracking:** reuse issue trackers and project notes. Don't create handoff files for routine features.

---

## Companion Coordination (`repo-native-refactor`)

Use at most one companion pass when the user requests review, concrete unresolved concerns remain, or a substantial contract, ownership, or semantic change warrants a scoped audit. Lightweight fixes do not trigger an automatic pass. Read [references/companion.md](references/companion.md) when a pass is warranted; finish normally if the companion is unavailable. Rerun affected checks after its edits; same-agent self-review is not independent review.

---

## Reference routing

Read supporting references only when the corresponding trigger occurs:

- **[references/bootstrap.md](references/bootstrap.md):** Read in **Bootstrap mode** to establish a new repository, set up minimal tooling, and build the first representative slice.
- **[references/evolution.md](references/evolution.md):** Read in **Evolve mode** to assess blast radius, handle breaking contract changes, or reconcile conflicting conventions.
- **[references/continuity.md](references/continuity.md):** Read when resuming work across sessions, taking over a repository, or reconciling stale notes with code reality.
- **[references/verification.md](references/verification.md):** Read when designing checks for greenfield code, high-risk boundaries (auth, data loss, concurrency), or weak test suites.
- **[references/shared-contracts.md](references/shared-contracts.md):** Canonical contract + evidence hierarchy + final-state rule. Read when touching any public interface, reconciling conflicting requirements, or certifying completion.
- **[references/migration-examples.md](references/migration-examples.md):** Atomic vs transitional migration patterns. Read in Evolve mode before mutating persisted state.
- **[references/companion.md](references/companion.md):** Full companion coordination (roles, handoff, loop limits). Read when planning a refactor pass with `repo-native-refactor`.

---

## Examples

### Add a feature on an existing foundation

```text
Use repo-foundation to add pagination to this project's existing search endpoint.
Preserve the current default response and my uncommitted changes. Reuse the
project's conventions, add relevant regression coverage, and verify the final diff.
```

Select Continue mode, inspect the endpoint's callers and baseline checks, implement
the smallest compatible change, and report the checks actually performed.

### Migrate an authorized persisted contract

```text
Use repo-foundation to migrate our local JSON store from schema v1 to v2.
Update the in-scope callers and tests. A failed migration must leave the existing
store intact; verify that failure boundary before reporting completion.
```

Select Evolve mode and read the migration and verification references before
changing persisted state. Establish the authorized target schema and verify the
transition, including failure-state preservation.

## Limitations

- Repository instructions and actual callers are required to establish local contracts; the skill cannot infer missing product requirements reliably.
- Atomic replacement examples depend on the target filesystem and do not establish crash durability on every platform.
- Relevant passing checks establish only their exercised scope; they do not prove that all requirements or failure modes are covered.
- Companion review is optional when unavailable; same-agent self-review is not independent review.

## Security & Safety Notes

This skill can edit source files and guide state migrations, so its declared risk
is `critical` under this collection's state-modification classification. Work only
within the user's authorized repository and task scope, preserve existing user
changes, and establish failure invariants before changing persisted data. Routine
implementation authority does not authorize pushing, publishing, deploying,
changing branch protection, installing system hooks, or purchases.

---

## When NOT to Use

- **Trivial edits:** Skip this skill for typos, isolated script adjustments, or formatting-only changes: the overhead is not worth it.


## Source & License

Adapted from [Natchannnn/repository-engineering-skills](https://github.com/Natchannnn/repository-engineering-skills/tree/e55b378158d5134a77af3b8dace4a2a1b17e41e2).
The original MIT copyright notice and license are retained in [references/LICENSE.md](references/LICENSE.md).
Collection adaptations add metadata, explicit triggers, interaction examples, limitations, and safety notes; the core workflow and supporting reference instructions are retained.
