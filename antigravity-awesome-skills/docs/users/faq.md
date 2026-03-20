# Frequently Asked Questions (FAQ)

**Got questions?** You're not alone! Here are answers to the most common questions about Antigravity Awesome Skills.

---

## General Questions

### What are "skills" exactly?

Skills are specialized instruction files that teach AI assistants how to handle specific tasks. Think of them as expert knowledge modules that your AI can load on-demand.
**Simple analogy:** Just like you might consult different experts (a lawyer, a doctor, a mechanic), these skills let your AI become an expert in different areas when you need them.

### Do I need to install every skill?

**No!** When you clone the repository, all skills are available, but your AI only loads them when you explicitly invoke them with `@skill-name`.
It's like having a library - all books are there, but you only read the ones you need.
**Pro Tip:** Use [Starter Packs](bundles.md) to focus on the skills that match your role first.

### What is the difference between Bundles and Workflows?

- **Bundles** are curated recommendations grouped by role or domain.
- **Workflows** are ordered execution playbooks for concrete outcomes.

Use bundles when you are deciding _which skills_ to include. Use workflows when you need _step-by-step execution_.

Start from:

- [bundles.md](bundles.md)
- [workflows.md](workflows.md)

### Which AI tools work with these skills?

- ✅ **Claude Code** (Anthropic CLI)
- ✅ **Gemini CLI** (Google)
- ✅ **Codex CLI** (OpenAI)
- ✅ **Cursor** (AI IDE)
- ✅ **Antigravity IDE**
- ✅ **OpenCode**
- ✅ **Kiro CLI** (Amazon)
- ✅ **Kiro IDE** (Amazon)
- ✅ **AdaL CLI**
- ⚠️ **GitHub Copilot** (partial support via copy-paste)

### Are these skills free to use?

**Yes!** This repository is licensed under MIT License.

- ✅ Free for personal use
- ✅ Free for commercial use
- ✅ You can modify them

### How do these skills avoid overflowing the model context?

Some host tools (for example custom agents built on Jetski/Cortex + Gemini) might be tempted to **concatenate every `SKILL.md` file into a single system prompt**.  
This is **not** how this repository is designed to be used, and it will almost certainly overflow the model’s context window if you concatenate the whole repository into one prompt.

Instead, hosts should:

- use `data/skills_index.json` as a **lightweight manifest** for discovery; and
- load individual `SKILL.md` files **only when a skill is invoked** (e.g. via `@skill-id` in the conversation).

For a concrete example (including pseudo‑code) see:

- [`docs/integrations/jetski-cortex.md`](../integrations/jetski-cortex.md)

### Do skills work offline?

The skill files themselves are stored locally on your computer, but your AI assistant needs an internet connection to function.

---

## Security & Trust

### What do the Risk Labels mean?

We classify skills so you know what you're running. These values map directly to the `risk:` field in every `SKILL.md` frontmatter:

- 🔵 **`none`**: Pure reference or planning content — no shell commands, no mutations, no network access.
- ⚪ **`safe`**: Community skills that are non-destructive (read-only, planning, code review, analysis).
- 🔴 **`critical`**: Skills that modify files, drop data, use network scanners, or perform destructive actions. **Use with caution.**
- 🟣 **`offensive`**: Security-focused offensive techniques (pentesting, exploitation). **Authorized use only** — always confirm the target is in scope.
- ⬜ **`unknown`**: Legacy or unclassified content. Review the skill manually before use.

### Can these skills hack my computer?

**No.** Skills are text files. However, they _instruct_ the AI to run commands. If a skill says "delete all files", a compliant AI might try to do it.
_Always check the Risk label and review the code._

---

## Installation & Setup

### Where should I install the skills?

The universal path that works with most tools is `.agent/skills/`.

**Using npx:** `npx antigravity-awesome-skills` (or `npx github:sickn33/antigravity-awesome-skills` if you get a 404).

**Using git clone:**

```bash
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

**Tool-specific paths:**

- Claude Code: `.claude/skills/`
- Gemini CLI: `.gemini/skills/`
- Codex CLI: `.codex/skills/`
- Cursor: `.cursor/skills/` or project root

**Claude Code plugin marketplace alternative:**

```text
/plugin marketplace add sickn33/antigravity-awesome-skills
/plugin install antigravity-awesome-skills
```

This repository now includes `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` so Claude Code can install the same skill tree through the plugin marketplace.

### Does this work with Windows?

**Yes.** Use the standard install flow:

```bash
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

If you have an older clone created around the removed symlink workaround, reinstall into a fresh directory or rerun `npx antigravity-awesome-skills`.

### I hit a truncation or context crash loop on Windows. How do I recover?

If Antigravity or a Jetski/Cortex-based host keeps reopening into:

> `TrajectoryChatConverter: could not convert a single message before hitting truncation`

use the dedicated Windows recovery guide:

- [`windows-truncation-recovery.md`](windows-truncation-recovery.md)

It includes:

- the manual cleanup steps for broken Local Storage / Session Storage / IndexedDB state
- the default Antigravity Windows paths to back up first
- an optional batch script adapted from [issue #274](https://github.com/sickn33/antigravity-awesome-skills/issues/274)

### How do I update skills?

Navigate to your skills directory and pull the latest changes:

```bash
cd .agent/skills
git pull origin main
```

---

## Using Skills

> **💡 For a complete guide with examples, see [usage.md](usage.md)**

### How do I invoke a skill?

Use the `@` symbol followed by the skill name:

```bash
@brainstorming help me design a todo app
```

### Can I use multiple skills at once?

**Yes!** You can invoke multiple skills:

```bash
@brainstorming help me design this, then use @writing-plans to create a task list.
```

### How do I know which skill to use?

1. **Browse the catalog**: Check the [Skill Catalog](../../CATALOG.md).
2. **Search**: `ls skills/ | grep "keyword"`
3. **Ask your AI**: "What skills do you have for testing?"

---

## Troubleshooting

### My AI assistant doesn't recognize skills

**Possible causes:**

1. **Wrong installation path**: Check your tool's docs. Try `.agent/skills/`.
2. **Restart Needed**: Restart your AI/IDE after installing.
3. **Typos**: Did you type `@brain-storming` instead of `@brainstorming`?

### A skill gives incorrect or outdated advice

Please [Open an issue](https://github.com/sickn33/antigravity-awesome-skills/issues)!
Include:

- Which skill
- What went wrong
- What should happen instead

---

## Contribution

### I'm new to open source. Can I contribute?

**Absolutely!** We welcome beginners.

- Fix typos
- Add examples
- Improve docs
  Check out [CONTRIBUTING.md](../../CONTRIBUTING.md) for instructions.

### My PR failed "Quality Bar" check. Why?

The repository enforces automated quality control. Your skill might be missing:

1. A valid `description`.
2. Usage examples.
   Run `npm run validate` locally to check before you push.

### My PR failed "security docs" check. What should I do?

Run the security docs gate locally and address the findings:

```bash
npm run security:docs
```

Common fixes:

- Replace risky examples like `curl ... | bash`, `wget ... | sh`, `irm ... | iex` with safer alternatives.
- Remove or redact token-like command-line examples.
- For intentional high-risk guidance, add explicit justification via:

```markdown
<!-- security-allowlist: reason and scope -->
```

### My PR triggered the `skill-review` automated check. What is it?

Since v8.0.0, GitHub automatically runs a `skill-review` workflow on any PR that adds or modifies a `SKILL.md` file. It reviews your skill against the quality bar and flags common issues — missing sections, weak triggers, or risky command patterns.

**If it reports findings:**

1. Open the **Checks** tab on your PR and read the `skill-review` job output.
2. Address any **actionable** findings (missing "When to Use", unclear triggers, blocked security patterns).
3. Push a new commit to the same branch — the check reruns automatically.

You do not need to close and reopen the PR. Informational or style-only findings do not block merging.

### Can I update an "Official" skill?

**No.** Official skills (in `skills/official/`) are mirrored from vendors. Open an issue instead.

---

## Pro Tips

- Start with `@brainstorming` before building anything new
- Use `@systematic-debugging` when stuck on bugs
- Try `@test-driven-development` for better code quality
- Explore `@skill-creator` to make your own skills

**Still confused?** [Open a discussion](https://github.com/sickn33/antigravity-awesome-skills/discussions) and we'll help you out! 🙌
