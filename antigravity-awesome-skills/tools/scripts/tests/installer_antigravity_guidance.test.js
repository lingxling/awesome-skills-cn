const assert = require("assert");
const path = require("path");

const installer = require(path.resolve(__dirname, "..", "..", "bin", "install.js"));

assert.deepStrictEqual(
  installer.buildCloneArgs("https://example.com/repo.git", "/tmp/skills"),
  ["clone", "--depth", "1", "https://example.com/repo.git", "/tmp/skills"],
  "installer should use a shallow clone by default",
);

assert.deepStrictEqual(
  installer.buildCloneArgs("https://example.com/repo.git", "/tmp/skills", "v1.2.3"),
  ["clone", "--depth", "1", "--branch", "v1.2.3", "https://example.com/repo.git", "/tmp/skills"],
  "installer should keep versioned installs shallow while selecting the requested ref",
);

const antigravityMessages = installer.getPostInstallMessages([
  { name: "Antigravity", path: "/tmp/.gemini/antigravity/skills" },
]);

assert.ok(
  antigravityMessages.some((message) => message.includes("agent-overload-recovery.md")),
  "Antigravity installs should point users to the overload recovery guide",
);
assert.ok(
  antigravityMessages.some((message) => message.includes("activate-skills.sh")),
  "Antigravity installs should mention the Unix activation flow",
);
assert.ok(
  antigravityMessages.some((message) => message.includes("activate-skills.bat")),
  "Antigravity installs should mention the Windows activation flow",
);

const codexMessages = installer.getPostInstallMessages([
  { name: "Codex CLI", path: "/tmp/.codex/skills" },
]);

assert.strictEqual(
  codexMessages.some((message) => message.includes("agent-overload-recovery.md")),
  false,
  "Non-Antigravity installs should not emit the Antigravity-specific overload hint",
);
