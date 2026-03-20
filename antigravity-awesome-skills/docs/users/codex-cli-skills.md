# Codex CLI Skills

If you want **Codex CLI skills** that are easy to install and practical in a local coding loop, this repository is designed for that exact use case.

Antigravity Awesome Skills supports Codex CLI through the `.codex/skills/` path and gives you a wide set of reusable task playbooks for planning, implementation, debugging, testing, security review, and delivery.

## Why use this repo for Codex CLI

- It supports Codex CLI with a dedicated install flag and a standard skills layout.
- It is strong for local repo work where you want to move from planning to implementation to verification without changing libraries.
- It includes both general-purpose engineering skills and deeper specialist tracks.
- It gives you docs and bundles, not just raw skill files.

## Install Codex CLI Skills

```bash
npx antigravity-awesome-skills --codex
```

### Verify the install

```bash
test -d .codex/skills || test -d ~/.codex/skills
```

## Best starter skills for Codex CLI

- [`brainstorming`](../../skills/brainstorming/): clarify requirements before touching code.
- [`concise-planning`](../../skills/concise-planning/): turn ambiguous work into an atomic execution plan.
- [`test-driven-development`](../../skills/test-driven-development/): structure changes around red-green-refactor.
- [`lint-and-validate`](../../skills/lint-and-validate/): keep quality checks close to the implementation loop.
- [`create-pr`](../../skills/create-pr/): wrap up work cleanly once implementation is done.

## Example Codex CLI prompts

```text
Use @concise-planning to break this feature request into an implementation checklist.
```

```text
Use @test-driven-development to add tests before changing this parser.
```

```text
Use @create-pr once everything is passing and summarize the user-facing changes.
```

## What to do next

- Read [`ai-agent-skills.md`](ai-agent-skills.md) if you want a framework for choosing between broad and curated skill libraries.
- Use [`workflows.md`](workflows.md) when you want step-by-step execution patterns for common engineering goals.
- Return to [`README.md`](../../README.md) for the full compatibility matrix.
