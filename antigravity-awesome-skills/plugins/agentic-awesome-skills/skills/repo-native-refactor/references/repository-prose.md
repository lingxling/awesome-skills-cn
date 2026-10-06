# Repository-native prose

Source prose should carry information that code cannot express clearly and should sound normal for its repository. The objective is not to imitate a person or evade detection. It is to remove narration, inflation, and generic language while preserving contracts and rationale.

## Resolve the local prose baseline

Before changing prose, sample healthy code near the same owner, domain, and runtime boundary. Infer only what the sample supports:

- which constructs are documented;
- comment density and placement;
- fragments versus complete sentences;
- capitalization and punctuation;
- docstring or API-documentation format;
- domain terminology and abbreviations;
- accepted tags such as `TODO`, `FIXME`, or issue references;
- whether test names, logs, and errors follow stable templates.

Prefer explicit repository configuration and documentation over inference. Do not treat newly introduced code, generated output, or a visibly inconsistent file as authoritative precedent.

Classify the baseline as `observed`, `likely`, `conflicting`, or `unknown`. If conventions conflict, prefer the pattern closest in ownership and domain. If evidence remains weak, use the conservative fallback below rather than inventing a house style.

## Distinguish prose surfaces

Do not apply one cleanup policy to every string.

### Internal comments

Internal comments may be removed when they merely repeat code. They are valuable when they explain a non-obvious constraint, invariant, tradeoff, external-system behavior, or reason an apparently simpler implementation is unsafe.

### Public documentation

Docstrings, API comments, annotations, and generated-documentation sources may be contracts or required by repository tooling. Preserve required structure and describe observable behavior accurately. Do not remove documentation merely because names and types look self-explanatory.

### Tests

Test descriptions and assertion messages should express behavior in the repository's established vocabulary. Avoid tutorial-like narratives and verbose restatements of the fixture. Treat expected messages and snapshots as behavioral evidence, not casual prose.

### Errors, logs, and command output

Error text, log templates, structured field names, metrics, events, stdout, and stderr may be consumed by tests, dashboards, alerts, scripts, or external systems. Treat them as observable behavior until callers and repository evidence establish otherwise.

### User-facing copy

Do not rewrite product text as code cleanup. Change it only when the task authorizes copy changes or the current wording is an established defect within scope.

## Decide: delete, preserve, tighten, correct, or report

### Delete

Delete prose that contributes no information beyond the code, including confirmed examples of:

- execution narration such as "first", "next", or "finally";
- comments that restate an assignment, branch, loop, guard, or function call;
- headings that divide a short function into obvious stages;
- implementation diary entries;
- comments added only to label ordinary getters, setters, constructors, or data movement;
- docstrings that repeat the symbol name and type information without adding a contract;
- claims that code is clean, simple, robust, elegant, or maintainable.

Prefer deletion over replacing a redundant long comment with a redundant short one.

### Preserve

Preserve still-relevant information about:

- compatibility behavior;
- external protocol irregularities;
- security boundaries;
- concurrency, ordering, transaction, or lifecycle constraints;
- counterintuitive domain rules;
- intentional degradation or best-effort behavior;
- performance tradeoffs that are not apparent locally;
- rationale supported by repository history or documentation.

Awkward wording alone is not enough to delete important knowledge.

### Tighten

Tighten prose when it contains necessary information but is inflated, generic, or poorly aligned with local terminology. Keep the concrete constraint and remove ceremony.

For example, replace:

```text
Gracefully handle the legacy response to ensure that the operation remains robust.
```

with a repository-appropriate form of:

```text
The v1 endpoint returns 200 with an empty body when the record is missing.
```

Do not add certainty that the evidence does not support.

### Correct

Correct stale or misleading prose only when behavior and intent are established. Update the smallest relevant surface. If correcting the prose exposes an actual behavioral defect, classify that code change separately.

### Report

Report rather than rewrite when a comment may encode history, a string may be consumed, or the intended contract is unclear. Uncertainty is not permission to normalize.

## Comment necessity test

Before retaining or adding a comment, ask:

> If this prose disappeared, would a maintainer lose an important fact that the code, type system, tests, or nearby contract does not express clearly?

If not, omit the comment. If yes, state the missing fact directly and at the narrowest useful location.

## Candidate signals, not deletion rules

The following patterns often deserve inspection:

- "We need to", "This function", or "The following code";
- "First", "Next", "Finally", or numbered step comments;
- "Handle gracefully", "ensure correctness", or "properly validate" without a named invariant;
- "robust", "seamless", "comprehensive", "elegant", or similar ungrounded claims;
- banners and separators that create visual ceremony without structural meaning;
- a comment before nearly every small block;
- repeated `@param` or return prose that adds nothing beyond types;
- comments explaining that code exists "for clarity" or "for maintainability";
- comments that describe the implementation process rather than lasting system behavior.

These are discovery hints only. Phrase matching, comment-count targets, and AI detectors cannot determine whether prose is correct or necessary.

## Conservative fallback

When the repository provides little reliable prose evidence:

- prefer no comment when code is already clear;
- explain why, a constraint, or external behavior rather than narrating what;
- use concrete domain nouns and active phrasing;
- keep one idea per comment;
- place the explanation next to the boundary it qualifies;
- avoid tutorial voice, self-dialogue, marketing language, and performative assurances;
- do not add comments merely to signal craftsmanship;
- do not invent tickets, incidents, owners, dates, or production history.
- Never invent ticket, PR, or incident references. An inaccessible or unverified reference is not evidence of fabrication. Preserve existing references unless repository evidence establishes that they are incorrect or obsolete; report material uncertainty instead of deleting them.

This fallback is deliberately modest. It must not become a universal style imposed over repository evidence.

## Final prose review

Inspect the final diff and ask:

- Did any deleted comment contain a constraint not preserved elsewhere?
- Did a rewrite become less precise while becoming shorter?
- Did redundant prose survive only in paraphrased form?
- Did comment density move toward relevant healthy code rather than an arbitrary target?
- Did terminology match the owning domain?
- Did any error, log, event, test expectation, or command output change without contract analysis?
- Did the refactor fabricate rationale or history?
- Is each added ticket, PR, or incident reference supported by a source?
- Was any existing reference deleted merely because it could not be verified?

Remove prose edits that cannot be justified by semantics or repository evidence.
