const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");

const { listSkillIds } = require("../../lib/skill-utils");

function withTempDir(fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "skill-utils-security-"));
  try {
    fn(dir);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

withTempDir((root) => {
  const skillsDir = path.join(root, "skills");
  const outsideDir = path.join(root, "outside-secret");

  fs.mkdirSync(skillsDir, { recursive: true });
  fs.mkdirSync(outsideDir, { recursive: true });

  fs.mkdirSync(path.join(skillsDir, "safe-skill"));
  fs.writeFileSync(path.join(skillsDir, "safe-skill", "SKILL.md"), "# safe\n");

  fs.writeFileSync(path.join(outsideDir, "SKILL.md"), "# secret\n");
  fs.symlinkSync(outsideDir, path.join(skillsDir, "linked-secret"));

  const skillIds = listSkillIds(skillsDir);

  assert.deepStrictEqual(
    skillIds,
    ["safe-skill"],
    "symlinked skill directories must not be treated as local skills",
  );
});
