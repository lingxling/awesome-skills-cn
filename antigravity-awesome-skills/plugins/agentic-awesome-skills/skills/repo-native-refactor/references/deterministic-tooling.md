# Deterministic tooling policy

Use deterministic tools for problems they can reliably establish.

Examples:

- formatter;
- compiler;
- type checker;
- linter;
- dependency graph analysis;
- dead-code analysis;
- security scanning;
- AST/CST structural matching.

Tool output is evidence, not architectural authority.

## Project tools first

Prefer tools already configured by the repository.

Do not install a new slop scanner or refactoring dependency merely because this skill mentions one.

Use repository configuration when available.

## Structural search and rewrite

AST/CST tools are strong for locating syntactic patterns.

They do not prove semantic equivalence.

Regex and text search may locate prose candidates such as step narration, repeated docstrings, or section banners. They cannot determine whether a comment carries a contract, historical constraint, or operational rationale. Never auto-delete or rewrite prose solely from a phrase match, comment-density target, or AI-detector score.

`ast-grep` can display or interactively apply rewrites, while `--update-all/-U` accepts every matching rewrite without confirmation. Therefore unattended bulk application is appropriate only for transformations already classified as mechanically safe.

Do not bulk-rewrite:

- exception ownership;
- fallback behavior;
- retry;
- authorization;
- transaction semantics;
- unresolved type mismatches;
- async error behavior.

## Dead-code and dependency analysis

Unused-code tools build a model of repository reachability.

A reported unused file/export/dependency may reflect:

- missing entry points;
- dynamic imports;
- plugin registration;
- generated files;
- incomplete framework integration;
- analyzer configuration gaps.

Knip documentation explicitly describes these situations and recommends correcting module-graph/configuration understanding rather than blindly suppressing or deleting findings.

Before deletion:

1. determine why the analyzer considers the item unreachable;
2. check framework/runtime discovery;
3. check generated references;
4. verify entry/plugin configuration;
5. delete only when semantic ownership confirms it is dead.

## Suppression policy

Do not respond to surprising findings by immediately adding ignores or suppression.

First determine whether:

- the code is actually dead;
- analyzer configuration is incomplete;
- the tool does not model the framework behavior.

Suppression should document a known limitation, not hide unexplained evidence.

## Tool confidence

Classify findings:

**Confirmed:** tool result plus repository evidence agree.

**Probable:** tool result plausible but not fully established.

**Uncertain:** analyzer limitations or runtime behavior may invalidate it.

When two repository tools disagree, the dynamic-entry check (imports, plugin
registration, generated references, entry configuration) wins over static
reachability claims. A scanner cannot declare dead what the runtime can load.

Only confirmed findings should drive destructive automated changes.

## Prose diagnostics

Use deterministic prose scans only to build an inspection queue. A useful diagnostic reports location and pattern without asserting authorship or defect status.

Do not install an AI detector or generic slop scanner merely to approve a refactor. If such a tool already exists in repository workflow, treat its output as a secondary signal and require repository evidence before mutation.
