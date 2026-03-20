const assert = require("assert");
const fs = require("fs");
const path = require("path");

const repoRoot = path.resolve(__dirname, "../..", "..");
const pycacheDir = path.join(repoRoot, "skills", "ui-ux-pro-max", "scripts", "__pycache__");
const syncRecommended = fs.readFileSync(
  path.join(repoRoot, "tools", "scripts", "sync_recommended_skills.sh"),
  "utf8",
);
const alphaVantage = fs.readFileSync(
  path.join(repoRoot, "skills", "alpha-vantage", "SKILL.md"),
  "utf8",
);

assert.strictEqual(
  fs.existsSync(pycacheDir),
  false,
  "tracked Python bytecode should not ship in skill directories",
);
assert.match(syncRecommended, /cp -RP/, "recommended skills sync should preserve symlinks instead of dereferencing them");
assert.doesNotMatch(syncRecommended, /for item in \*\/; do\s+rm -rf "\$item"/, "recommended skills sync must not delete matched paths via naive glob iteration");
assert.match(syncRecommended, /readlink|test -L|find .* -type d/, "recommended skills sync should explicitly avoid following directory symlinks during cleanup");
assert.doesNotMatch(alphaVantage, /--- Unknown/, "alpha-vantage frontmatter should not contain malformed delimiters");
