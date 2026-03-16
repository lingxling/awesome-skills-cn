const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");

const { resolveSafeRealPath } = require("../../lib/symlink-safety");

function withTempDir(fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "symlink-safety-"));
  try {
    fn(dir);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

withTempDir((root) => {
  const safeRoot = path.join(root, "safe-root");
  const internalDir = path.join(safeRoot, "internal");
  const outsideDir = path.join(root, "outside");
  const internalLink = path.join(safeRoot, "internal-link");
  const outsideLink = path.join(safeRoot, "outside-link");

  fs.mkdirSync(internalDir, { recursive: true });
  fs.mkdirSync(outsideDir, { recursive: true });
  fs.writeFileSync(path.join(internalDir, "data.txt"), "ok");
  fs.writeFileSync(path.join(outsideDir, "secret.txt"), "secret");

  fs.symlinkSync(internalDir, internalLink);
  fs.symlinkSync(outsideDir, outsideLink);

  const internalResolved = resolveSafeRealPath(safeRoot, internalLink);
  const outsideResolved = resolveSafeRealPath(safeRoot, outsideLink);

  assert.strictEqual(internalResolved, fs.realpathSync(internalDir));
  assert.strictEqual(outsideResolved, null);
});
