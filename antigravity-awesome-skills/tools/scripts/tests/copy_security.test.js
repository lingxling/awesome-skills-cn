const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");

const { copyRecursiveSync } = require("../../bin/install");

async function main() {
  const { copyFolderSync } = await import("../../scripts/setup_web.js");

  const root = fs.mkdtempSync(path.join(os.tmpdir(), "copy-security-"));
  try {
    const safeRoot = path.join(root, "safe-root");
    const destRoot = path.join(root, "dest-root");
    const outsideDir = path.join(root, "outside");

    fs.mkdirSync(path.join(safeRoot, "nested"), { recursive: true });
    fs.mkdirSync(outsideDir, { recursive: true });

    fs.writeFileSync(path.join(safeRoot, "nested", "ok.txt"), "ok");
    fs.writeFileSync(path.join(outsideDir, "secret.txt"), "secret");
    fs.symlinkSync(outsideDir, path.join(safeRoot, "escape-link"));

    copyRecursiveSync(safeRoot, path.join(destRoot, "install-copy"), safeRoot);
    copyFolderSync(safeRoot, path.join(destRoot, "web-copy"), safeRoot);

    assert.strictEqual(
      fs.existsSync(path.join(destRoot, "install-copy", "escape-link", "secret.txt")),
      false,
      "installer copy must not follow symlinks outside the cloned root",
    );
    assert.strictEqual(
      fs.existsSync(path.join(destRoot, "web-copy", "escape-link", "secret.txt")),
      false,
      "web setup copy must not follow symlinks outside the skills root",
    );
    assert.strictEqual(
      fs.readFileSync(path.join(destRoot, "install-copy", "nested", "ok.txt"), "utf8"),
      "ok",
    );
    assert.strictEqual(
      fs.readFileSync(path.join(destRoot, "web-copy", "nested", "ok.txt"), "utf8"),
      "ok",
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
