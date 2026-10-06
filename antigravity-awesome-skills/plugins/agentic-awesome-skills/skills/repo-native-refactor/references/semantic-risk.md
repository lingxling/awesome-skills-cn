# Semantic risk and mutation policy

> Field note: when unsure between R2 and R3, I pick the higher band. Cheaper than a rollback.

Risk measures the potential consequence of being wrong.

Transformation safety measures confidence that a rewrite preserves meaning.

They are related but separate.

## R0 - mechanical

Typical examples:

- formatting;
- import ordering;
- provably unused imports;
- obvious accidental separators;
- deterministic syntax normalization.
- deletion of a locally obvious comment that only restates syntax and carries no contract.

Policy:

Automatic mutation is acceptable when repository tooling establishes the transformation.

## R1 - low structural risk

Typical examples:

- redundant local syntax;
- provably dead local residue;
- obvious no-op indirection.
- comment or docstring cleanup whose meaning is fully established locally.

Policy:

Mutation is acceptable when scope is local and verification is straightforward.

## R2 - contextual structural risk

Typical examples:

- renaming;
- moving code;
- extracting or inlining helpers;
- reducing nesting;
- consolidating duplication;
- collapsing abstractions.
- rewriting rationale, public documentation, test descriptions, or potentially consumed text.

Policy:

Inspect ownership and repository precedent first.

Require a concrete maintainability or semantic benefit.

Do not refactor merely because another form is prettier.

## R3 - semantic risk

Typical examples:

- exception propagation;
- fallbacks;
- retries;
- timeout;
- caching;
- serialization;
- transaction ownership;
- async lifecycle;
- resource cleanup.
- error or operational wording known to participate in application behavior.

Policy:

Never bulk-rewrite.

Establish the preservation contract and meaningful behavioral verification.

## R4 - critical boundary

Typical examples:

- authentication;
- authorization;
- permissions;
- payment;
- cryptography;
- migrations;
- destructive persistence;
- concurrency-critical logic;
- security enforcement.

Policy:

Maximum conservatism.

When evidence is incomplete, preserve behavior and report the finding.

## Transformation classes

### Class A - proven mechanical

May be applied unattended.

The rewrite must have clear local equivalence or be an established project-tool transformation.

### Class B - context sensitive

Generate or consider a candidate change, then inspect and verify.

Examples:

- helper inline;
- control-flow flattening;
- rename;
- abstraction removal;
- context-sensitive comment or documentation changes.

### Class C - semantic

Requires reasoning about behavioral ownership.

Examples:

- changing `catch` behavior;
- replacing fallbacks with exceptions;
- changing retries;
- changing transaction scope;
- changing auth logic;
- changing async error ownership.

Never run Class C as a mass structural rewrite.

## Prose risk

Prose risk depends on its role, not its appearance.

- Deleting a confirmed syntax restatement may be mechanical.
- Rewriting a rationale requires repository and behavioral context.
- Public API documentation may define a contract.
- Error messages, logs, event fields, snapshots, stdout, and stderr may be observable behavior.
- Comments around security, compatibility, transactions, concurrency, migrations, or lifecycle inherit the risk of the behavior they explain.

Phrase matching can find candidates but cannot establish a transformation class.

## Justification gate

Before a significant R2+ mutation establish:

**Observed problem:** What is wrong?

**Consequence:** Why does it matter?

**Owner:** Which layer should own the correction?

**Repository evidence:** What supports that decision?

**Minimal correction:** What is the smallest adequate repair?

**Preservation:** What behavior must remain unchanged?

**Verification:** How will the correction be checked?

If the only justification is “cleaner”, “more elegant”, or “more senior”, do not perform a broad refactor.

**Visible-text escalation:** if a structural change alters user- or contract-visible text
(error messages, CLI output, logs, event fields, snapshots), escalate one band
(R1-R2, R2-R3) and treat that text as an observable contract: preserve it exactly or
update its consumers within scope. A green suite that asserts only exception types does
not prove the text is safe to change.

## Stop conditions

Preserve rather than aggressively refactor when:

- intended behavior cannot be established;
- tests and implementation conflict without clear authority;
- repository patterns conflict materially;
- public contract consequences are unknown;
- migration intent is unclear;
- error ownership cannot be determined;
- concurrency behavior lacks verification;
- duplicate-looking implementations may represent independent domains;
- unusual code may encode an unexplained historical constraint.

A stop applies to the uncertain region, not necessarily the entire audit.
