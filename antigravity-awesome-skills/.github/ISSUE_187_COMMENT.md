Suggested comment for [Issue #187](https://github.com/sickn33/antigravity-awesome-skills/issues/187). Paste this on the issue:

---

Great questions! Here are answers to both:

---

### 1. Global rule for Context7 alongside skills

**Yes, it is absolutely worth it.** Context7 and skills serve different purposes and are fully complementary:

- **Skills** provide process guidance, domain expertise, workflows, and best-practice checklists. They tell the AI *how* to approach a task.
- **Context7** (`@context7-auto-research`) fetches *live, up-to-date documentation* for the specific library or framework version you are actually using. Skills cannot replace this—they have no mechanism to pull current API references at runtime.

Recommended global rule (add to your `CLAUDE.md` or project settings):

```
When working with any library, framework, or external API, use Context7 to fetch
current documentation before writing or reviewing code.
```

This ensures the AI doesn't rely on potentially outdated training data for fast-moving ecosystems (Next.js app router, Prisma, shadcn/ui, etc.).

---

### 2. Maintaining development state across chat sessions

There is a **built-in skill system** for exactly this: the **Conductor** workflow. You don't need to manually request summaries every time—you just set it up once and it self-maintains.

#### How it works

Conductor keeps all project state in a `conductor/` directory that lives alongside your code:

```
conductor/
├── index.md          ← read this at the start of every session
├── product.md        ← what you're building and why
├── tech-stack.md     ← your dependencies and architecture decisions
├── workflow.md       ← your dev practices and quality gates
├── tracks.md         ← registry of all tasks (your todo.md equivalent)
└── tracks/
    └── <feature-id>/
        ├── spec.md   ← acceptance criteria
        ├── plan.md   ← task checklist with [x]/[~]/[ ] status
        └── metadata.json ← progress counters, current task
```

`tracks.md` + `plan.md` are the living task.md/todo.md you were looking for. Every completed task, phase, and decision is committed to git alongside the code.

#### Getting started

| Command | What it does |
|---|---|
| `/conductor:setup` | One-time setup — creates all context files interactively |
| `/conductor:new-track "description"` | Creates a spec + phased plan for a new feature/fix |
| `/conductor:implement` | Executes the next pending task, updating plan.md as it goes |
| `/conductor:status` | Shows overall progress, active track, next actions |

#### Starting a new session reliably

At the top of any new chat, ask the AI to:

```
Read conductor/index.md, then conductor/tracks.md, then the plan.md
for any in-progress track. Summarise where we left off and what the
next task is.
```

Because every completed task is marked `[x]` and committed, the AI will always reconstruct the exact state — no manual summary needed.

#### Relevant skills to install

```bash
# One-time project setup
npx antigravity-awesome-skills add conductor-setup

# Day-to-day development
npx antigravity-awesome-skills add conductor-status
npx antigravity-awesome-skills add conductor-implement
npx antigravity-awesome-skills add conductor-new-track

# For deeper session continuity reading
npx antigravity-awesome-skills add context-driven-development
npx antigravity-awesome-skills add context-management-context-save
npx antigravity-awesome-skills add context-management-context-restore
```

Hope this helps — welcome to the community! 🎉
