const assert = require("assert");
const fs = require("fs");
const path = require("path");

const repoRoot = path.resolve(__dirname, "../..", "..");

const compactScript = fs.readFileSync(
  path.join(repoRoot, "skills", "cc-skill-strategic-compact", "suggest-compact.sh"),
  "utf8",
);
const wsListener = fs.readFileSync(
  path.join(repoRoot, "skills", "videodb", "scripts", "ws_listener.py"),
  "utf8",
);

assert.match(compactScript, /XDG_STATE_HOME/, "strategic compact counter should use a user-owned state directory");
assert.doesNotMatch(compactScript, /\/tmp\/claude-tool-count/, "strategic compact counter must not use predictable /tmp files");
assert.match(wsListener, /XDG_STATE_HOME/, "videodb listener should default to a user-owned state directory");
assert.doesNotMatch(wsListener, /VIDEODB_EVENTS_DIR", "\/tmp"/, "videodb listener must not default to /tmp");
