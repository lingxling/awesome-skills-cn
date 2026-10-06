# Repository Rehabilitation

Use this mode only when the authorized scope is codebase-wide or spans multiple coherent domains. Its purpose is consistent rehabilitation, not a single sweeping rewrite.

## Survey before mutation

Map the repository at the level needed to choose safe batches:

- instruction and ownership boundaries;
- applications, packages, modules, or domains;
- public, persistence, network, security, and operational boundaries;
- generated, vendored, migrated, snapshot, and golden artifacts;
- build, type, lint, test, generation, and validation workflows;
- areas with active user changes;
- duplicated systems for errors, validation, configuration, persistence, or observability;
- areas where repository conventions conflict.

Do not review every file at equal depth. Begin with architecture signals, representative healthy paths, changed or high-churn areas when known, and boundaries that determine behavior.

## Build a concise repository profile

Record only decisions that will guide multiple batches:

- ownership and dependency direction;
- domain vocabulary;
- type, schema, and validation boundaries;
- error and result model;
- persistence and transaction conventions;
- async, retry, timeout, and cancellation ownership;
- logging and observability conventions;
- test strategy and trustworthy verification commands;
- comment and documentation conventions;
- dependency policy;
- sensitive or excluded artifacts;
- observed conflicts and unresolved uncertainty.

Mark each convention `observed`, `likely`, `conflicting`, or `unknown`. Cite the repository evidence used to infer it. Keep the profile compact and task-local unless the user asks to add documentation to the repository.

Do not infer standards from generated code, obvious outliers, or the code currently suspected of being low quality.

## Choose calibration work

Start with a representative, low-to-moderate-risk batch that has meaningful verification. Use it to test whether the repository profile produces a native result before applying it broadly.

Avoid beginning with authentication, payments, migrations, destructive persistence, or concurrency-critical code unless those areas are the explicit task and have adequate evidence.

## Batch by ownership

A batch should normally share a domain, owner, runtime boundary, and verification path. It should be small enough that a maintainer can understand its purpose and inspect every changed line.

For each batch:

1. confirm scope and preservation contracts;
2. refine only the relevant part of the repository profile;
3. inventory and classify findings;
4. apply the smallest justified corrections;
5. run focused verification;
6. inspect the diff and remove unjustified changes;
7. record residual uncertainty before continuing.

Do not mix unrelated naming, dependency, architecture, and formatting campaigns in one batch.

## Update the profile carefully

New evidence may refine the profile. It should not silently reverse decisions already used elsewhere.

When a later domain follows a different valid convention, scope the convention to that domain instead of forcing global uniformity. When patterns genuinely conflict, preserve both until ownership or migration intent establishes a preferred direction.

## Cross-batch review

After the bounded passes, inspect the combined result for:

- duplicated concepts left under different names;
- accidental cross-domain coupling;
- inconsistent error, validation, or schema boundaries;
- prose or terminology that diverges between equivalent owners;
- dependencies introduced only to support cleanup;
- broad formatting noise;
- verification gaps that compound across batches.

Run repository-level validation only after focused checks are stable. A clean full-suite result does not excuse an incoherent or unreviewable combined diff.

## Stop conditions

Pause expansion into a region when:

- its owner or intended behavior cannot be established;
- its convention conflicts materially with the current profile;
- meaningful verification is unavailable for high-risk behavior;
- it contains unrelated active changes;
- generated or historical workflow is unclear;
- cleanup would require redesign beyond the authorized scope.

Continue elsewhere when safe. Repository-wide authorization broadens coverage, not semantic permission.
