Hi @adamgyongyosi! 👋

I see you're asking about **bundles** (I think you meant "bundle" not "bundel"). Great question!

### What are Bundles?

**Bundles** in this repository are **curated collections of skills** grouped together by role, expertise level, or use case. Think of them like "starter packs" that help you quickly get the right set of skills for your needs without being overwhelmed by the 1,200+ available skills.

### How Bundles Work

Bundles are defined in the [`build-catalog.js`](https://github.com/sickn33/antigravity-awesome-skills/blob/main/tools/scripts/build-catalog.js#L322-L415) file. The system automatically groups skills based on keywords found in their tags, names, and descriptions. Currently, there are **5 core bundles**:

1. **`core-dev`** - Core development skills (Python, JavaScript, TypeScript, Go, Rust, Java, React, APIs, etc.)
2. **`security-core`** - Security, privacy, and compliance essentials
3. **`k8s-core`** - Kubernetes and service mesh essentials
4. **`data-core`** - Data engineering and analytics foundations
5. **`ops-core`** - Operations, observability, and delivery pipelines

### How to Use Bundles on WSL2 Debian 13 with Antigravity

Since you're using **WSL2 Debian 13 with Antigravity**, here's how to work with bundles:

#### 1. **View Available Bundles**

Check out the complete bundle documentation:
- 📖 [Bundles Documentation](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)

#### 2. **Choose Your Bundle**

Pick a bundle based on your needs. For example:
- Building web apps? → `core-dev` bundle
- Working on security? → `security-core` bundle
- DevOps work? → `ops-core` bundle

#### 3. **Use Skills from Your Bundle**

In Antigravity, you reference skills directly in your prompts. For example:

```bash
# Use a skill by name
antigravity "Use python-pro to help me refactor this code"

# Or reference specific skills
antigravity "Use fastapi-pro to create a REST API"
```

### Quick Start Commands

```bash
# 1. If you haven't cloned the repo yet
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills

# 2. View the generated bundles data
cat data/bundles.json

# 3. Browse skills in a bundle
# The bundles.json file lists all skills that belong to each bundle
```

### Additional Resources

- 📖 [Complete Usage Guide](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/usage.md)
- 📦 [Full Bundles Guide](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- 🚀 [Getting Started](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/getting-started.md)

Hope this helps! Let me know if you have any other questions. 😊