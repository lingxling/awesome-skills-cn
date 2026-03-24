#!/usr/bin/env node

const { spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");
const { resolveSafeRealPath } = require("../lib/symlink-safety");

const REPO = "https://github.com/sickn33/antigravity-awesome-skills.git";
const HOME = process.env.HOME || process.env.USERPROFILE || "";

function resolveDir(p) {
  if (!p) return null;
  const s = p.replace(/^~($|\/)/, HOME + "$1");
  return path.resolve(s);
}

function parseArgs() {
  const a = process.argv.slice(2);
  let pathArg = null;
  let versionArg = null;
  let tagArg = null;
  let cursor = false,
    claude = false,
    gemini = false,
    codex = false,
    antigravity = false,
    kiro = false;

  for (let i = 0; i < a.length; i++) {
    if (a[i] === "--help" || a[i] === "-h") return { help: true };
    if (a[i] === "--path" && a[i + 1]) {
      pathArg = a[++i];
      continue;
    }
    if (a[i] === "--version" && a[i + 1]) {
      versionArg = a[++i];
      continue;
    }
    if (a[i] === "--tag" && a[i + 1]) {
      tagArg = a[++i];
      continue;
    }
    if (a[i] === "--cursor") {
      cursor = true;
      continue;
    }
    if (a[i] === "--claude") {
      claude = true;
      continue;
    }
    if (a[i] === "--gemini") {
      gemini = true;
      continue;
    }
    if (a[i] === "--codex") {
      codex = true;
      continue;
    }
    if (a[i] === "--antigravity") {
      antigravity = true;
      continue;
    }
    if (a[i] === "--kiro") {
      kiro = true;
      continue;
    }
    if (a[i] === "install") continue;
  }

  return {
    pathArg,
    versionArg,
    tagArg,
    cursor,
    claude,
    gemini,
    codex,
    antigravity,
    kiro,
  };
}

function getTargets(opts) {
  const targets = [];
  if (opts.pathArg) {
    return [{ name: "Custom", path: resolveDir(opts.pathArg) }];
  }
  if (opts.cursor) {
    targets.push({ name: "Cursor", path: path.join(HOME, ".cursor", "skills") });
  }
  if (opts.claude) {
    targets.push({ name: "Claude Code", path: path.join(HOME, ".claude", "skills") });
  }
  if (opts.gemini) {
    targets.push({ name: "Gemini CLI", path: path.join(HOME, ".gemini", "skills") });
  }
  if (opts.codex) {
    const codexHome = process.env.CODEX_HOME;
    const codexPath = codexHome
      ? path.join(codexHome, "skills")
      : path.join(HOME, ".codex", "skills");
    targets.push({ name: "Codex CLI", path: codexPath });
  }
  if (opts.kiro) {
    targets.push({ name: "Kiro", path: path.join(HOME, ".kiro", "skills") });
  }
  if (opts.antigravity) {
    targets.push({ name: "Antigravity", path: path.join(HOME, ".gemini", "antigravity", "skills") });
  }
  if (targets.length === 0) {
    targets.push({ name: "Antigravity", path: path.join(HOME, ".gemini", "antigravity", "skills") });
  }
  return targets;
}

function printHelp() {
  console.log(`
antigravity-awesome-skills — installer

  npx antigravity-awesome-skills [install] [options]

  Clones the skills repo into your agent's skills directory.

Options:
  --cursor       Install to ~/.cursor/skills (Cursor)
  --claude       Install to ~/.claude/skills (Claude Code)
  --gemini       Install to ~/.gemini/skills (Gemini CLI)
  --codex        Install to ~/.codex/skills (Codex CLI)
  --kiro         Install to ~/.kiro/skills (Kiro CLI)
  --antigravity  Install to ~/.gemini/antigravity/skills (Antigravity)
  --path <dir>   Install to <dir> (default: ~/.gemini/antigravity/skills)
  --version <ver>  After clone, checkout tag v<ver> (e.g. 4.6.0 -> v4.6.0)
  --tag <tag>      After clone, checkout this tag (e.g. v4.6.0)

Examples:
  npx antigravity-awesome-skills
  npx antigravity-awesome-skills --cursor
  npx antigravity-awesome-skills --kiro
  npx antigravity-awesome-skills --antigravity
  npx antigravity-awesome-skills --version 4.6.0
  npx antigravity-awesome-skills --path ./my-skills
  npx antigravity-awesome-skills --claude --codex    Install to multiple targets
`);
}

function copyRecursiveSync(src, dest, rootDir = src, skipGit = true) {
  const stats = fs.lstatSync(src);
  const resolvedSource = stats.isSymbolicLink()
    ? resolveSafeRealPath(rootDir, src)
    : src;

  if (!resolvedSource) {
    console.warn(`  Skipping symlink outside cloned skills root: ${src}`);
    return;
  }

  const resolvedStats = fs.statSync(resolvedSource);
  if (resolvedStats.isDirectory()) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(resolvedSource).forEach((child) => {
      if (skipGit && child === ".git") return;
      copyRecursiveSync(path.join(resolvedSource, child), path.join(dest, child), rootDir, skipGit);
    });
  } else {
    fs.copyFileSync(resolvedSource, dest);
  }
}

/** Copy contents of repo's skills/ into target so each skill is target/skill-name/ (for Claude Code etc.). */
function installSkillsIntoTarget(tempDir, target) {
  const repoSkills = path.join(tempDir, "skills");
  if (!fs.existsSync(repoSkills)) {
    console.error("Cloned repo has no skills/ directory.");
    process.exit(1);
  }
  fs.readdirSync(repoSkills).forEach((name) => {
    const src = path.join(repoSkills, name);
    const dest = path.join(target, name);
    copyRecursiveSync(src, dest, repoSkills);
  });
  const repoDocs = path.join(tempDir, "docs");
  if (fs.existsSync(repoDocs)) {
    const docsDest = path.join(target, "docs");
    if (!fs.existsSync(docsDest)) fs.mkdirSync(docsDest, { recursive: true });
    copyRecursiveSync(repoDocs, docsDest, repoDocs);
  }
}

function run(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, { stdio: "inherit", ...opts });
  if (r.status !== 0) process.exit(r.status == null ? 1 : r.status);
}

function installForTarget(tempDir, target) {
  if (fs.existsSync(target.path)) {
    const gitDir = path.join(target.path, ".git");
    if (fs.existsSync(gitDir)) {
      console.log(`  Migrating from full-repo install to skills-only layout…`);
      const backupPath = `${target.path}_backup_${Date.now()}`;
      try { 
        const stats = fs.lstatSync(target.path);
        const isSymlink = stats.isSymbolicLink();
        const symlinkTarget = isSymlink ? 
        fs.readlinkSync(target.path) : null;
        fs.renameSync(target.path, backupPath);
        console.log(`  ⚠️  Safety Backup created at: ${backupPath}`);
        if (isSymlink) {
          fs.symlinkSync(symlinkTarget, target.path, 'dir');
        } else {
          fs.mkdirSync(target.path, { recursive: true, mode: stats.mode });
        }
      } catch (err) {
        console.error(`  Migration Error: ${err.message}`);
        process.exit(1);
      }
    } else {
      console.log(`  Updating existing install at ${target.path}…`);
    }
  } else {
    const parent = path.dirname(target.path);
    if (!fs.existsSync(parent)) {
      try {
        fs.mkdirSync(parent, { recursive: true });
      } catch (e) {
        console.error(`  Cannot create parent directory: ${parent}`, e.message);
        process.exit(1);
      }
    }
    fs.mkdirSync(target.path, { recursive: true });
  }

  installSkillsIntoTarget(tempDir, target.path);
  console.log(`  ✓ Installed to ${target.path}`);
}

function getPostInstallMessages(targets) {
  const messages = [
    "Pick a bundle in docs/users/bundles.md and use @skill-name in your AI assistant.",
  ];

  if (targets.some((target) => target.name === "Antigravity")) {
    messages.push(
      "If Antigravity hits context/truncation limits, see docs/users/agent-overload-recovery.md",
    );
    messages.push(
      "For clone-based installs, use scripts/activate-skills.sh or scripts/activate-skills.bat",
    );
  }

  return messages;
}

function main() {
  const opts = parseArgs();
  const { tagArg, versionArg } = opts;

  if (opts.help) {
    printHelp();
    return;
  }

  const targets = getTargets(opts);
  if (!targets.length || !HOME) {
    console.error(
      "Could not resolve home directory. Use --path <absolute-path>.",
    );
    process.exit(1);
  }

  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "ag-skills-"));
  const originalCwd = process.cwd();

  try {
    console.log("Cloning repository…");
    run("git", ["clone", REPO, tempDir]);

    const ref =
      tagArg ||
      (versionArg
        ? versionArg.startsWith("v")
          ? versionArg
          : `v${versionArg}`
        : null);
    if (ref) {
      console.log(`Checking out ${ref}…`);
      process.chdir(tempDir);
      run("git", ["checkout", ref]);
      process.chdir(originalCwd);
    }

    console.log(`\nInstalling for ${targets.length} target(s):`);
    for (const target of targets) {
      console.log(`\n${target.name}:`);
      installForTarget(tempDir, target);
    }

    for (const message of getPostInstallMessages(targets)) {
      console.log(`\n${message}`);
    }
  } finally {
    try {
      if (fs.existsSync(tempDir)) {
        if (fs.rmSync) {
          fs.rmSync(tempDir, { recursive: true, force: true });
        } else {
          fs.rmdirSync(tempDir, { recursive: true });
        }
      }
    } catch (e) {
      // ignore cleanup errors
    }
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  copyRecursiveSync,
  getPostInstallMessages,
  installSkillsIntoTarget,
  installForTarget,
  main,
};
