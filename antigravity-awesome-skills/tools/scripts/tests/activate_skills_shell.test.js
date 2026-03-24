const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const repoRoot = path.resolve(__dirname, "../..", "..");
const scriptPath = path.join(repoRoot, "scripts", "activate-skills.sh");

const root = fs.mkdtempSync(path.join(os.tmpdir(), "activate-skills-shell-"));
const baseDir = path.join(root, "antigravity");
const repoSkills = path.join(root, "repo-skills");

function makeSkill(skillId) {
  const skillDir = path.join(repoSkills, skillId);
  fs.mkdirSync(skillDir, { recursive: true });
  fs.writeFileSync(
    path.join(skillDir, "SKILL.md"),
    `---\nname: ${skillId}\ndescription: test skill\ncategory: testing\nrisk: safe\nsource: community\ndate_added: "2026-03-22"\n---\n`,
    "utf8",
  );
}

try {
  makeSkill("brainstorming");
  makeSkill("systematic-debugging");
  makeSkill("custom-skill");

  const result = spawnSync(
    "bash",
    [scriptPath, "--clear", "brainstorming", "custom-skill"],
    {
      cwd: repoRoot,
      env: {
        ...process.env,
        AG_BASE_DIR: baseDir,
        AG_REPO_SKILLS_DIR: repoSkills,
        AG_PYTHON_BIN: "python3",
      },
      encoding: "utf8",
    },
  );

  assert.strictEqual(result.status, 0, result.stderr || result.stdout);
  assert.ok(
    fs.existsSync(path.join(baseDir, "skills", "brainstorming", "SKILL.md")),
    "brainstorming should be activated into the live skills directory",
  );
  assert.ok(
    fs.existsSync(path.join(baseDir, "skills", "custom-skill", "SKILL.md")),
    "literal safe skill ids should be activated from the library",
  );
  assert.ok(
    fs.existsSync(path.join(baseDir, "skills_library", "brainstorming", "SKILL.md")),
    "repo skills should be synced into the backing library",
  );
  assert.match(
    result.stdout,
    /Done! Antigravity skills are now activated\./,
    "script should report successful activation",
  );
} finally {
  fs.rmSync(root, { recursive: true, force: true });
}
