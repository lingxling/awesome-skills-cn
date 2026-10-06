# Bootstrap: establishing foundation and initial slice

> Field note: I used to scaffold full layered dirs on day one. Deleted most of it. Now I ship one slice first.

Use this reference when starting a new repository from scratch or when setting up an area of an existing repository that lacks minimal tooling, conventions, or architecture.

---

## 1. Minimal inputs and scoping

Before generating code or directory structures, establish the critical constraints.
First: what should the software actually do for an outside observer (CLI command, HTTP endpoint, UI component, library export, worker process)? Second: hard constraints (language, runtime, frameworks, persistence, external services, anything operational the user asked for). Third, sort decisions into two piles.
Reversible assumptions cover directory structure, utility naming, standard library picks, and helper layout. Choose conventionally on your own. Don't ask permission for every folder or variable name.
Product decisions cover persistence store, auth architecture, vendors, and breaking domain rules. Bundle missing product decisions into one short question before implementing.

---

## 2. The first representative slice

Avoid horizontal layering without working behavior. Do not generate empty directories, unused interfaces, speculative repositories, or generic wrappers that serve no active flow.

Build a single, real, end-to-end slice that crosses the system's primary architectural boundaries. The shapes below are illustrative examples, not mandatory architectures:

| Project Type | Example Slice Shape (Illustrative) |
|---|---|
| **CLI Tool** | Input parsing (flags/arguments) → core logic → observable output and exit status. (A simple tool does not require multiple internal layers). |
| **API / Service** | Request intake → route handler → domain logic/validation → response. (Persistence is included only if the service actually requires state; stateless services, proxies, and aggregators do not need persistence layers). |
| **Web / UI** | User interaction/event → state transition/store update → observable UI rendering (including empty/loading/error states). |
| **Library / Package** | Public API export → core implementation → return value / error handling. (Libraries do not need an app server or startup daemon). |
| **Worker / Job** | Task intake/deserialization → business processing → outcome persistence, acknowledgment, or retry handling. |

Verify both the successful path and meaningful domain failure modes (e.g., validation failure, not found, unauthenticated).

If external integrations cannot be run locally, simulated stubs are permitted only when explicitly acknowledged; never describe a mock integration as real.

---

## 3. Tooling and instructions setup

Establish the minimal commands necessary for an agent or developer to run and verify the project using stack-native configuration:

1. **Native configuration:** Place commands in standard stack files (`package.json`, `pyproject.toml`, `Makefile`, `Cargo.toml`, `go.mod`, etc.).
2. **Commands fit the project type:**
   - Run/start command for local execution (only when applicable; libraries and utility packages do not need a start command).
   - Test command executing automated checks.
   - Lint/format command if idiomatic to the stack.
3. **Instructions handling:**
   - If the repository already has an instructions file (e.g., `AGENTS.md` or `README.md`), update it minimally only if needed to record new commands or invariants. Never overwrite or recreate existing instructions just because you are in Bootstrap mode.
   - If no instructions file exists and the host/workflow uses one, create a concise file (around 300–700 tokens) pointing to commands and noting key constraints.

---

## 4. Establishing reference code

Code created during bootstrap serves as precedent for future development only when it satisfies all of the following:

1. **Traceable:** Directly satisfies a concrete user requirement or contract.
2. **Observable verification:** Accompanied by automated checks whose expected values reflect business outcomes rather than copying internal implementation details.
3. **Appropriate ownership and dependencies:** Modules have clear responsibilities and dependency directions suited to the chosen architecture and actual project requirements, without forcing unnecessary layers (e.g., transport/domain/persistence separation is not required for a small CLI, library, or script).
4. **No unexplained debt:** Contains no unexplained workarounds, commented-out dead code, or temporary hacks.
5. **Bounded scope:** If a convention applies only to a specific module, document it as module-local rather than an overarching repository standard.

No code pattern is permanently "golden." When requirements change or architecture evolves, update reference paths rather than maintaining obsolete conventions.
