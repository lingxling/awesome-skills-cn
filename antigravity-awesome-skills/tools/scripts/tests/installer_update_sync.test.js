const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const installer = require(path.resolve(__dirname, "..", "..", "bin", "install.js"));

function writeSkill(repoRoot, skillName, content = "# Skill\n") {
  const skillDir = path.join(repoRoot, "skills", skillName);
  fs.mkdirSync(skillDir, { recursive: true });
  fs.writeFileSync(path.join(skillDir, "SKILL.md"), content, "utf8");
}

function createFakeRepo(rootDir, skills) {
  fs.mkdirSync(path.join(rootDir, "skills"), { recursive: true });
  for (const skillName of skills) {
    writeSkill(rootDir, skillName, `# ${skillName}\n`);
  }
}

function readManifestEntries(targetDir) {
  const manifestPath = path.join(targetDir, ".antigravity-install-manifest.json");
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  return manifest.entries;
}

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), "installer-update-sync-"));

try {
  const repoV1 = path.join(tmpRoot, "repo-v1");
  const repoV2 = path.join(tmpRoot, "repo-v2");
  const targetDir = path.join(tmpRoot, "target");
  fs.mkdirSync(targetDir, { recursive: true });

  createFakeRepo(repoV1, ["skill-a", "skill-b"]);
  createFakeRepo(repoV2, ["skill-a"]);

  installer.installForTarget(repoV1, { name: "Test", path: targetDir });
  assert.ok(fs.existsSync(path.join(targetDir, "skill-a", "SKILL.md")));
  assert.ok(fs.existsSync(path.join(targetDir, "skill-b", "SKILL.md")));

  installer.installForTarget(repoV2, { name: "Test", path: targetDir });
  assert.ok(fs.existsSync(path.join(targetDir, "skill-a", "SKILL.md")));
  assert.strictEqual(
    fs.existsSync(path.join(targetDir, "skill-b")),
    false,
    "stale managed skill should be pruned during updates",
  );
  assert.deepStrictEqual(
    readManifestEntries(targetDir),
    ["skill-a"],
    "install manifest should mirror the latest installed entries",
  );

  const badTargetPath = path.join(tmpRoot, "bad-target");
  fs.writeFileSync(badTargetPath, "not-a-directory", "utf8");
  const badTargetCheck = spawnSync(
    process.execPath,
    [
      "-e",
      `
const installer = require(${JSON.stringify(path.resolve(__dirname, "..", "..", "bin", "install.js"))});
installer.installForTarget(${JSON.stringify(repoV2)}, { name: "BadTarget", path: ${JSON.stringify(badTargetPath)} });
`,
    ],
    {
      stdio: "pipe",
      encoding: "utf8",
    },
  );

  assert.notStrictEqual(
    badTargetCheck.status,
    0,
    "installer should fail fast when target path exists as a non-directory",
  );
  assert.match(
    `${badTargetCheck.stdout}\n${badTargetCheck.stderr}`,
    /not a directory/i,
    "installer should print a clear error for non-directory targets",
  );
} finally {
  fs.rmSync(tmpRoot, { recursive: true, force: true });
}
