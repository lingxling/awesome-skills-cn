const assert = require("assert");
const fs = require("fs");
const path = require("path");
const { findProjectRoot } = require("../../lib/project-root");

const projectRoot = findProjectRoot(__dirname);
const marketplacePath = path.join(projectRoot, ".claude-plugin", "marketplace.json");
const marketplace = JSON.parse(fs.readFileSync(marketplacePath, "utf8"));

assert.ok(Array.isArray(marketplace.plugins), "marketplace.json must define a plugins array");
assert.ok(marketplace.plugins.length > 0, "marketplace.json must contain at least one plugin");

for (const plugin of marketplace.plugins) {
  assert.strictEqual(
    typeof plugin.source,
    "string",
    `plugin ${plugin.name || "<unnamed>"} must define source as a string`,
  );
  assert.ok(
    plugin.source.startsWith("./"),
    `plugin ${plugin.name || "<unnamed>"} source must be a relative path starting with ./`,
  );
}

console.log("ok");
