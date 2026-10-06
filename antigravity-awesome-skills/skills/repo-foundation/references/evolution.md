# Evolution: adapting architecture and contracts

Use this reference when a task alters core contracts, architectural boundaries, or domain ownership, or when working in a repository with conflicting conventions.

---

## 1. Intentional contract changes vs. regressions

When requirements evolve, contracts must adapt. Tell intent apart from regression: an intentional change alters public API signatures, schemas, data models, or error codes because the user explicitly asked for new behavior. A regression is an unintended break in existing functionality.
Accept what the user requested. Don't fight explicit requests by forcing compatibility with deprecated behavior. Foundation and refactor work both accommodate authorized changes while preserving untouched contracts.

---

## 2. Blast radius assessment

Before mutating shared contracts, determine the blast radius:

1. **Identify callers and consumers:** Locate all internal modules, external consumers, database schemas, message queues, or serialized data structures affected by the change.
2. **Boundary scope:** Confirm whether the change can be completed within the authorized scope or if it requires updating multiple subsystem boundaries.
3. When all callers reside within the codebase and are under the current task's scope, update the contract, callers, and tests together (the atomic update). When consumers are external, persisted data must be migrated, or callers span multiple independent services, maintain a compatibility bridge, migration script, or dual-read/write strategy as requested (the transitional migration).

---

## 3. Controlled migration workflow

Execute architectural adjustments in logical order:

1. **Update contract definitions:** Modify the authoritative interfaces, schemas, or type definitions first.
2. **Migrate callers:** Update calling code, dependency injection bindings, and data transformations to use the new contract.
3. **Align tests:** Update existing tests that assert the old contract so they verify the new behavior. Add tests covering edge cases and error semantics of the new contract.
4. **Synchronize documentation:** Update repository instructions, schema definitions, and API documentation to prevent stale instructions from misleading future agents.

---

## 4. Reconciling conflicting repository conventions

In mature repositories, different modules often reflect different architectural eras or styles:

When patterns conflict, resolve using evidence hierarchy in order:
  1. User's explicit instruction for the current task.
  2. Documented architecture and repository instructions.
  3. Preserved public contracts and persisted schemas.
  4. Healthy sibling code within the *same* owning domain and runtime boundary.
  5. Relevant tests, schemas, callers, and dependencies.
  6. Local module conventions.
Do not rewrite healthy sibling code in another module merely to match your current change. Preserve legitimate domain-specific differences unless codebase-wide unification is explicitly requested; premature homogenization helps no one.
If existing code contains obvious workarounds or defects, do not replicate them in new code. Follow the healthiest precedent within the domain: defects never become precedent.

---

## 5. Multi-pressure checklist

When migration, risk, docs, and workspace pressures stack (the usual evolution mess),
work in this order and do not skip steps:

1. Baseline: record revision, failing checks, and uncommitted user work.
2. Protect user work: distinct-region edits only; stop on real collision.
3. Reconcile docs against code reality before mutating (code describes behavior, docs get fixed after).
4. Highest-risk caller first with maximum conservatism; atomic path for the rest.
5. Rerun affected checks on the final tree; report what remains red and why.
