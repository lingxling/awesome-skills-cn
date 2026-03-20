const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");

async function main() {
  const { copyIndexFiles } = await import("../../scripts/setup_web.js");

  const root = fs.mkdtempSync(path.join(os.tmpdir(), "setup-web-sync-"));
  try {
    const source = path.join(root, "skills_index.json");
    const dest = path.join(root, "public", "skills.json");
    const backup = path.join(root, "public", "skills.json.backup");

    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(source, JSON.stringify([{ id: "demo", category: "testing" }], null, 2));

    copyIndexFiles(source, dest, backup);

    assert.deepStrictEqual(
      JSON.parse(fs.readFileSync(dest, "utf8")),
      JSON.parse(fs.readFileSync(source, "utf8")),
    );
    assert.deepStrictEqual(
      JSON.parse(fs.readFileSync(backup, "utf8")),
      JSON.parse(fs.readFileSync(source, "utf8")),
    );
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
