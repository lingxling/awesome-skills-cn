#!/usr/bin/env node

const { spawnSync } = require("child_process");
const path = require("path");

const NETWORK_TEST_ENV = "ENABLE_NETWORK_TESTS";
const ENABLED_VALUES = new Set(["1", "true", "yes", "on"]);
const TOOL_SCRIPTS = path.join("tools", "scripts");
const TOOL_TESTS = path.join(TOOL_SCRIPTS, "tests");
const LOCAL_TEST_COMMANDS = [
  [path.join(TOOL_TESTS, "validate_skills_headings.test.js")],
  [path.join(TOOL_SCRIPTS, "run-python.js"), path.join(TOOL_TESTS, "test_validate_skills_headings.py")],
];
const NETWORK_TEST_COMMANDS = [
  [path.join(TOOL_SCRIPTS, "run-python.js"), path.join(TOOL_TESTS, "inspect_microsoft_repo.py")],
  [path.join(TOOL_SCRIPTS, "run-python.js"), path.join(TOOL_TESTS, "test_comprehensive_coverage.py")],
];

function isNetworkTestsEnabled() {
  const value = process.env[NETWORK_TEST_ENV];
  if (!value) {
    return false;
  }
  return ENABLED_VALUES.has(String(value).trim().toLowerCase());
}

function runNodeCommand(args) {
  const result = spawnSync(process.execPath, args, { stdio: "inherit" });

  if (result.error) {
    throw result.error;
  }

  if (result.signal) {
    process.kill(process.pid, result.signal);
  }

  if (typeof result.status !== "number") {
    process.exit(1);
  }

  if (result.status !== 0) {
    process.exit(result.status);
  }
}

function runCommandSet(commands) {
  for (const commandArgs of commands) {
    runNodeCommand(commandArgs);
  }
}

function main() {
  const mode = process.argv[2];

  if (mode === "--local") {
    runCommandSet(LOCAL_TEST_COMMANDS);
    return;
  }

  if (mode === "--network") {
    runCommandSet(NETWORK_TEST_COMMANDS);
    return;
  }

  runCommandSet(LOCAL_TEST_COMMANDS);

  if (!isNetworkTestsEnabled()) {
    console.log(
      `[tests] Skipping network integration tests. Set ${NETWORK_TEST_ENV}=1 to enable.`,
    );
    return;
  }

  console.log(`[tests] ${NETWORK_TEST_ENV} enabled; running network integration tests.`);
  runCommandSet(NETWORK_TEST_COMMANDS);
}

main();
