const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");

const installer = require(path.resolve(__dirname, "..", "..", "bin", "install.js"));

function withTempDir(fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "installer-filters-"));
  try {
    fn(dir);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

function writeSkill(repoRoot, skillPath, frontmatter) {
  const skillDir = path.join(repoRoot, "skills", skillPath);
  fs.mkdirSync(skillDir, { recursive: true });
  fs.writeFileSync(
    path.join(skillDir, "SKILL.md"),
    `---\n${frontmatter}\n---\n\n# ${skillPath}\n`,
    "utf8",
  );
}

assert.deepStrictEqual(
  installer.parseSelectorArg("safe,critical,offensive-"),
  { include: ["safe", "critical"], exclude: ["offensive"] },
  "parseSelectorArg should split CSV values and treat suffix - as exclude",
);

assert.deepStrictEqual(
  installer.parseSelectorArg("safe,safe-,none"),
  { include: ["none"], exclude: ["safe"] },
  "parseSelectorArg should let excludes win over duplicate includes",
);

assert.strictEqual(
  installer.isOpenCodeStylePath(path.join("/tmp", ".agents", "skills")),
  true,
  "OpenCode-style paths should be detected from .agents/skills",
);

assert.strictEqual(
  installer.isOpenCodeStylePath(path.join("/tmp", ".codex", "skills")),
  false,
  "non-OpenCode paths should not trigger the .agents/skills guidance",
);

withTempDir((root) => {
  const repoRoot = path.join(root, "repo");
  fs.mkdirSync(path.join(repoRoot, "skills"), { recursive: true });
  fs.mkdirSync(path.join(repoRoot, "docs"), { recursive: true });

  writeSkill(
    repoRoot,
    "safe-debugger",
    'name: safe-debugger\ncategory: development\nrisk: safe\ntags: [debugging, typescript]',
  );
  writeSkill(
    repoRoot,
    "offensive-tool",
    'name: offensive-tool\ncategory: security\nrisk: offensive\ntags: [pentest, red-team]',
  );
  writeSkill(
    repoRoot,
    path.join("nested", "metadata-tags"),
    'name: metadata-tags\ncategory: backend\nrisk: none\nmetadata:\n  tags: "api,saas"',
  );

  assert.deepStrictEqual(
    installer.getInstallEntries(repoRoot, installer.buildInstallSelectors({})),
    ["nested/metadata-tags", "offensive-tool", "safe-debugger", "docs"],
    "full installs should return recursive skill paths plus docs",
  );

  assert.deepStrictEqual(
    installer.getInstallEntries(
      repoRoot,
      installer.buildInstallSelectors({
        riskArg: "safe,none",
        categoryArg: "development,backend",
        tagsArg: "typescript,saas",
      }),
    ),
    ["nested/metadata-tags", "safe-debugger", "docs"],
    "filters should AND across flags and keep docs when skills match",
  );

  assert.deepStrictEqual(
    installer.getInstallEntries(
      repoRoot,
      installer.buildInstallSelectors({
        tagsArg: "pentest-",
      }),
    ),
    ["nested/metadata-tags", "safe-debugger", "docs"],
    "exclude-only tag filters should remove matching skills",
  );

  assert.strictEqual(
    installer.matchesInstallSelectors(
      { risk: "safe", category: "development", tags: ["debugging", "typescript"] },
      installer.buildInstallSelectors({
        riskArg: "safe",
        categoryArg: "development",
        tagsArg: "typescript",
      }),
    ),
    true,
    "skills should match when all selector dimensions pass",
  );

  assert.strictEqual(
    installer.matchesInstallSelectors(
      { risk: "", category: "development", tags: ["debugging"] },
      installer.buildInstallSelectors({
        riskArg: "safe",
      }),
    ),
    false,
    "missing scalar metadata should not satisfy positive selectors",
  );

  const openCodeMessages = installer.getPostInstallMessages(
    [{ name: "Custom", path: path.join(root, ".agents", "skills") }],
    installer.buildInstallSelectors({}),
  );

  assert.ok(
    openCodeMessages.some((message) => message.includes("reduced install")),
    "OpenCode-style paths should get reduced-install guidance",
  );

  const filteredOpenCodeMessages = installer.getPostInstallMessages(
    [{ name: "Custom", path: path.join(root, ".agents", "skills") }],
    installer.buildInstallSelectors({ categoryArg: "development" }),
  );

  assert.strictEqual(
    filteredOpenCodeMessages.some((message) => message.includes("Example:")),
    false,
    "OpenCode guidance should skip the example once selectors are already active",
  );
});
