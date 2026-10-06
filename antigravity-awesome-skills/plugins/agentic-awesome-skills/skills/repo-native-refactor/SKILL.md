---
name: repo-native-refactor
description: "Review diffs without editing, or perform evidence-based cleanup while preserving authorized behavior, public contracts, and domain ownership."
category: development
risk: critical
source: https://github.com/Natchannnn/repository-engineering-skills
source_repo: Natchannnn/repository-engineering-skills
source_type: community
date_added: "2026-09-30"
author: Natchannnn
tags: [repository-engineering, code-review, refactoring, public-contracts]
tools: [codex]
license: MIT
license_source: https://github.com/Natchannnn/repository-engineering-skills/blob/e55b378158d5134a77af3b8dace4a2a1b17e41e2/LICENSE
metadata:
  version: "0.3.0"
  license: "MIT"
---

# Repo-native refactor

## When to Use

- Use when the user asks to review a diff, branch, or PR for correctness, contract breaks, or operational risk.
- Use when the user authorizes bounded cleanup before opening a PR or asks to consolidate duplicated policy with shared ownership.
- Use for repository rehabilitation only when the user explicitly requests work across multiple domains.
- Establish review-only, edit, or combined authority before choosing the operating mode.

Produce the smallest coherent change that belongs naturally in the target repository.

Prioritize in order:
1. **Correctness and security:** prevent regressions, avoid new security vulnerabilities, handle boundary conditions.
2. **Semantic integrity:** preserve existing invariants, state transitions, validation, and error boundaries.
3. **Contracts stay as declared:** the rule lives in `references/shared-contracts.md` §1. Preserve the authorized target contract; otherwise keep exact declared types. Internal helpers are fine when exposed contracts stay exact.
4. **Repository conformity:** match surrounding naming, domain conventions, and architectural precedents.
5. **Economy and simplicity:** minimal intervention. Delete dead weight, avoid premature abstractions.

This is a post-implementation audit and small cleanup skill. It is not permission to redesign the repository. Establish a concrete consequence such as inconsistent behavior, duplicated policy that must change together, unclear ownership, avoidable resource cost, or a demonstrated maintenance obstacle. Leave healthy code unchanged when the benefit is speculative.

---

## Minimal intervention and evidence gate

- **Evidence-based intervention:** refactor only with concrete evidence of divergence, defect, or operational risk. If greenfield code or an additive diff is already minimal, idiomatic, and passing, leave it. A pattern you recognize is a candidate finding, not a reason to change anything.
- **Semantic DRY (Cost-benefit consolidation):** merge duplicated logic only when the copies share an owner, an invariant, and a reason to change, and only if merging saves more than it costs. Leave similar-looking checks in separate domains alone, and keep small local duplication when merging would obscure ownership.
- **Contract boundary protection:** preserve public interfaces, parameter names, and return types, except where the task clearly authorizes the change. During cleanup, keep the authorized target contract; don't revert to the old one.

---

## Operating modes

- **Review vs. Refactor Authority:** first establish the outcome: findings, edits, or both. Review-only means inspection and verification, no source edits. Authorized cleanup allows bounded corrections; don't ask approval again for routine choices.
- **Change-set cleanup:** for a working tree, branch, commit range, feature, or bounded checkpoint. Work diff-first; read surrounding code only to understand ownership, contracts, and precedent.
- **Repository rehabilitation:** only when explicitly requested across multiple domains. Read [repository rehabilitation](references/repository-rehabilitation.md), build a short profile, and work in batches you can verify independently.

---

## Evidence hierarchy

Use the evidence hierarchy to guide investigation, not to resolve material contradictions automatically. Reconcile conflicting requirements, documentation, callers, and tests before changing the affected contract. When repository patterns conflict, resolve in order:
1. User requirements and explicitly authorized scope.
2. Documented architecture and repository guidelines.
3. Observable public contracts and persisted schemas.
4. Healthy sibling code within the same domain and runtime boundary.
5. Relevant tests, schemas, callers, and dependencies.
6. Dominant local conventions.
7. Language and runtime idioms.
8. Conservative, idiomatic defaults.

Never treat a temporary workaround, buggy sibling, or accidental pattern as precedent.

---

## Workflow

### 1. Establish scope and baseline
Before mutating code, identify:
- Comparison base and working-tree state.
- In-scope files vs. untouched user modifications.
- Existing verification commands and their current pass/fail status.

Differentiate pre-existing failures from regressions introduced by this pass. Never claim a check ran when it did not.

### 2. Establish intent, ownership, and preservation
Refactoring is behavior-preserving by default. Protect:
- Public APIs, serializations, and database schemas.
- Concurrency guarantees, idempotency, timeouts, and retries.
- Resource lifecycles (file handles, sockets, database transactions).

If a bug requires an observable change, classify and report it as an intentional behavioral correction rather than routine cleanup.

### 3. Inventory findings before rewriting
Inspect the authorized scope for:
- Validation or control flow whose structure obscures an invariant, creates inconsistent behavior, or duplicates the same owned policy.
- Misplaced domain ownership or leaky abstractions.
- Leaked unmanaged resources or missing atomic flush/sync calls.
- Unnecessary boilerplate, dead code, or commentary narrating syntax.

Read [finding taxonomy](references/finding-taxonomy.md) for complex cases. Establish the smallest adequate correction before editing.

### 4. Classify risk and refactor
Risk bands:
- **R0 - Mechanical:** Established formatter or locally provable cleanup.
- **R1 - Low Structural:** Local residue with straightforward test verification.
- **R2 - Contextual Structural:** Renames, control-flow changes, extraction of shared predicates.
- **R3 - Semantic:** Errors, fallbacks, retries, serialization, transactions, async, or lifecycles.
- **R4 - Critical Boundary:** Auth, permissions, crypto, data migrations, persistence durability.

Read [semantic risk](references/semantic-risk.md) for R2+ changes. Never mass-rewrite R3 or R4 behavior without explicit instructions and verified tests.

### 5. Audit code prose
- When prose is in scope, treat comments, docstrings, CLI output, and error messages as distinct surfaces. Read [repository prose](references/repository-prose.md) for that work.
- Delete comments that merely narrate obvious syntax or execution order.
- Preserve and tighten comments that explain non-obvious invariants, protocol quirks, rounding, or hardware workarounds.
- Never invent fictitious tickets, PR references, or production incident IDs.

### 6. Verify and review
- Run the smallest repository-native checks that meaningfully exercise the change. For R3/R4 changes or weak test suites, read [error and reliability boundaries](references/error-reliability.md) and [testing integrity](references/testing-integrity.md).
- Prioritize diff reviewability and coherence over raw line minimization; do not compress code into unreadable one-liners.
- Distinguish intentional behavioral corrections from mechanical cleanup.
- Review the final diff like a skeptical maintainer. Every line needs a reason. No contract changed without permission, no test got weaker, no dependency moved for nothing.

---

## Reference routing

Read supporting references only when the corresponding trigger occurs:

- **[references/shared-contracts.md](references/shared-contracts.md):** Canonical contract + evidence hierarchy. Read when touching any public interface or reconciling conflicts.
- **[references/refactor-examples.md](references/refactor-examples.md):** R0–R4 good/bad diffs. Read before rewriting a candidate finding.
- **[references/finding-taxonomy.md](references/finding-taxonomy.md):** Read for complex multi-smell diffs to name owner + consequence.
- **[references/semantic-risk.md](references/semantic-risk.md):** Read for R2+ changes, justification gate, and stop conditions.
- **[references/repository-prose.md](references/repository-prose.md):** Read when editing comments, docstrings, CLI output, or error messages.
- **[references/error-reliability.md](references/error-reliability.md) + [references/testing-integrity.md](references/testing-integrity.md):** Read for R3/R4 or weak test suites.
- **[references/deterministic-tooling.md](references/deterministic-tooling.md):** Read before introducing new scanners or bulk-codemod tools.
- **[references/repository-rehabilitation.md](references/repository-rehabilitation.md):** Read only for explicitly requested multi-domain rehabilitation, in verifiable batches.

---

## Hard stops

Do not force a refactor where intent, ownership, public-contract consequences, migration semantics, or concurrency behavior cannot be established. Do not guess between conflicting architectural patterns without evidence.

---

## Completion Report

Scale the completion report to the change. Omit empty sections. Format completion concisely:

### Result
Use one: **Verified**, **Verified with caveats**, **Needs review**, or **Failed verification**.

For review-only requests, an empty findings list is a complete result, not an
embarrassing one. Never manufacture findings to fill a report: each reported
finding needs a producer, a consumer, and an observed consequence, or it is
not reported.

### Changed
Summarize material corrections by file and function.

### Preserved intentionally
Note specific patterns or contracts deliberately retained to avoid breaking downstream consumers.

### Verification
List exact verification commands executed and their outcomes.

### Residual uncertainty
Document unresolved limitations or high-risk boundaries intentionally deferred.

---

## Examples

### Review without editing

```text
Use repo-native-refactor to review this branch against main for public-contract
breaks and retry failures. Do not edit source files. Report only findings with
a concrete producer, consumer, and observable consequence.
```

Inspect the comparison base and relevant callers, run proportionate verification,
and report evidence-backed findings. An empty findings list is a valid result.

### Consolidate one owned policy

```text
Use repo-native-refactor to consolidate the duplicated eligibility checks owned
by this billing module. Preserve the current accepted inputs, error types, and
return values. Leave similar checks in other domains alone and run the module's tests.
```

Confirm that the copies share an owner, invariant, and reason to change before
extracting anything. Keep the correction bounded and verify the final behavior.

## Limitations

- Review requires an identifiable comparison base and enough repository evidence to establish contracts and ownership.
- Similar syntax alone does not establish shared policy or justify consolidation.
- The skill cannot establish migration or concurrency safety without relevant requirements and verification; unresolved material uncertainty is a hard stop.
- Local checks and self-review do not establish independent review or universal reliability.

## Security & Safety Notes

Review-only mode permits inspection and verification without source edits. The
authorized cleanup mode can modify source files, so the declared risk is `critical`
under this collection's state-modification classification. Keep edits within the
user's authorized scope, preserve unrelated user changes, and apply the R3/R4
verification and stop conditions before changing sensitive behavior. Cleanup
authority does not authorize publishing, deploying, or changing external systems.

---

## When NOT to Use

- **Clean greenfield code:** Do not refactor newly written code that is already minimal, idiomatic, and passing all tests.
- **Speculative cleanup:** If you cannot state the domain owner and the concrete maintenance consequence in a single sentence, leave the code unmodified.
- **Risk classification:** When uncertain between risk bands (such as R2 structural vs. R3 semantic), default conservatively to the higher risk band and require explicit justification.


## Source & License

Adapted from [Natchannnn/repository-engineering-skills](https://github.com/Natchannnn/repository-engineering-skills/tree/e55b378158d5134a77af3b8dace4a2a1b17e41e2).
The original MIT copyright notice and license are retained in [references/LICENSE.md](references/LICENSE.md).
Collection adaptations add metadata, explicit triggers, interaction examples, limitations, and safety notes; the core workflow and supporting reference instructions are retained.
