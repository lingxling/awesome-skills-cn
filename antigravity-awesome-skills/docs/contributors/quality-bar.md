# 🏆 Quality Bar & Validation Standards

To transform **Antigravity Awesome Skills** from a collection of scripts into a trusted platform, every skill must meet a specific standard of quality and safety.

## The "Validated" Badge ✅

A skill earns the "Validated" badge only if it meets these **5 quality checks**. Some are enforced automatically today, while others still require reviewer judgment:

### 1. Metadata Integrity

The `SKILL.md` frontmatter must be valid YAML and contain:

- `name`: Kebab-case, matches folder name.
- `description`: Under 200 chars, clear value prop.
- `risk`: One of `[none, safe, critical, offensive, unknown]`. Use `unknown` only for legacy or unclassified skills; prefer a concrete level for new skills.
- `source`: URL to original source (or "self" if original).

### 2. Clear Triggers ("When to use")

The skill MUST have a section explicitly stating when to trigger it.

- **Good**: "Use when the user asks to debug a React component."
- **Bad**: "This skill helps you with code."
Accepted headings: `## When to Use`, `## Use this skill when`, `## When to Use This Skill`.

### 3. Safety & Risk Classification

Every skill must declare its risk level:

- 🟢 **none**: Pure text/reasoning (e.g., Brainstorming).
- 🔵 **safe**: Reads files, runs safe commands (e.g., Linter).
- 🟠 **critical**: Modifies state, deletes files, pushes to prod (e.g., Git Push).
- 🔴 **offensive**: Pentesting/Red Team tools. **MUST** have "Authorized Use Only" warning.

### 4. Copy-Pasteable Examples

At least one code block or interaction example that a user (or agent) can immediately use.

### 5. Explicit Limitations

A list of known edge cases or things the skill _cannot_ do.

- _Example_: "Does not work on Windows without WSL."

---

## Support Levels

We also categorize skills by who maintains them:

| Level         | Badge | Meaning                                             |
| :------------ | :---- | :-------------------------------------------------- |
| **Official**  | 🟣    | Maintained by the core team. High reliability.      |
| **Community** | ⚪    | Contributed by the ecosystem. Best effort support.  |
| **Verified**  | ✨    | Community skill that has passed deep manual review. |

---

## How to Validate Your Skill

The canonical validator is `tools/scripts/validate_skills.py`, but the recommended entrypoint is `npm run validate` before submitting a PR:

```bash
npm run validate
npm run validate:references
npm test
```

Notes:

- `npm run validate` is the operational contributor gate.
- `npm run validate:strict` is a useful hardening pass, but the repository still contains legacy skills that do not yet satisfy strict validation.
- Examples and limitations remain part of the quality bar even when they are not fully auto-enforced by the current validator.
