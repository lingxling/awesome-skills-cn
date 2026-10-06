"""Deterministic tests for the PyLabRobot offline planning CLIs."""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skills" / "pylabrobot"
TESTS_DIR = Path(__file__).resolve().parent
if str(SKILL_ROOT) not in sys.path:
  sys.path.insert(0, str(SKILL_ROOT))

from scripts import (  # noqa: E402
    check_deck_geometry,
    generate_simulation_plan,
    inspect_backends,
    plan_transfers,
    validate_manifest,
)


class CliTests(unittest.TestCase):
  def setUp(self) -> None:
    self.previous_cwd = Path.cwd()
    os.chdir(REPO_ROOT)

  def tearDown(self) -> None:
    os.chdir(self.previous_cwd)

  @staticmethod
  def run_main(function, arguments: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
      code = function(arguments)
    return code, stdout.getvalue(), stderr.getvalue()

  def test_all_help_paths_are_dependency_free(self) -> None:
    modules = (
        validate_manifest,
        check_deck_geometry,
        plan_transfers,
        generate_simulation_plan,
        inspect_backends,
    )
    for module in modules:
      output = io.StringIO()
      with self.subTest(module=module.__name__), redirect_stdout(output):
        with self.assertRaises(SystemExit) as raised:
          module.main(["--help"])
        self.assertEqual(raised.exception.code, 0)
        self.assertIn("usage:", output.getvalue())

  def test_manifest_and_geometry_pass(self) -> None:
    code, stdout, stderr = self.run_main(
        validate_manifest.main,
        ["--input", "tests/pylabrobot/fixtures/protocol_manifest.json"],
    )
    self.assertEqual((code, stderr), (0, ""))
    self.assertTrue(json.loads(stdout)["ok"])

    code, stdout, stderr = self.run_main(
        check_deck_geometry.main,
        ["--input", "tests/pylabrobot/fixtures/protocol_manifest.json"],
    )
    self.assertEqual((code, stderr), (0, ""))
    self.assertTrue(json.loads(stdout)["ok"])

  def test_collision_fixture_is_rejected(self) -> None:
    code, stdout, stderr = self.run_main(
        check_deck_geometry.main,
        ["--input", "tests/pylabrobot/fixtures/collision_manifest.json"],
    )
    self.assertEqual(stderr, "")
    self.assertEqual(code, 3)
    report = json.loads(stdout)
    self.assertFalse(report["ok"])
    self.assertEqual(
        report["collisions"],
        [{"resource_a": "source_plate", "resource_b": "destination_plate"}],
    )

  def test_transfer_ledger_and_tip_plan(self) -> None:
    code, stdout, stderr = self.run_main(
        plan_transfers.main,
        [
            "--manifest",
            "tests/pylabrobot/fixtures/protocol_manifest.json",
            "--transfers",
            "tests/pylabrobot/fixtures/transfers.csv",
        ],
    )
    self.assertEqual((code, stderr), (0, ""))
    report = json.loads(stdout)
    self.assertEqual(report["tip_summary"]["used"], 2)
    self.assertEqual(
        [operation["assigned_tip"] for operation in report["operations"]],
        ["tips:A1", "tips:B1"],
    )
    ledger = {
        row["location"]: row["volume_uL"]
        for row in report["final_volume_ledger"]
    }
    self.assertEqual(ledger["source_plate:A1"], 150.0)
    self.assertEqual(ledger["source_plate:B1"], 125.0)
    self.assertEqual(ledger["destination_plate:A1"], 50.0)
    self.assertEqual(ledger["destination_plate:B1"], 25.0)

  def test_generated_plan_cannot_enable_live_hardware(self) -> None:
    code, stdout, stderr = self.run_main(
        generate_simulation_plan.main,
        [
            "--manifest",
            "tests/pylabrobot/fixtures/protocol_manifest.json",
            "--transfers",
            "tests/pylabrobot/fixtures/transfers.csv",
        ],
    )
    self.assertEqual((code, stderr), (0, ""))
    report = json.loads(stdout)
    self.assertEqual(report["plan_kind"], "offline_review_only")
    self.assertFalse(report["live_backend_permitted"])
    self.assertFalse(report["connection_attempted"])
    self.assertFalse(report["serial_usb_network_access"])
    self.assertEqual(len(report["steps"]), 8)

  def test_duplicate_json_key_is_rejected(self) -> None:
    with tempfile.TemporaryDirectory(dir=TESTS_DIR) as directory:
      path = Path(directory) / "duplicate.json"
      path.write_text('{"schema_version":"1.0","schema_version":"1.0"}', encoding="utf-8")
      relative_path = path.relative_to(REPO_ROOT)
      code, stdout, stderr = self.run_main(
          validate_manifest.main,
          ["--input", str(relative_path)],
      )
    self.assertEqual((code, stdout), (2, ""))
    self.assertIn("duplicate JSON key", json.loads(stderr)["message"])

  def test_parent_directory_traversal_is_rejected(self) -> None:
    code, stdout, stderr = self.run_main(
        validate_manifest.main,
        ["--input", "tests/pylabrobot/fixtures/../fixtures/protocol_manifest.json"],
    )
    self.assertEqual((code, stdout), (2, ""))
    self.assertIn("traversal", json.loads(stderr)["message"])

  def test_backend_inspector_never_connects(self) -> None:
    code, stdout, stderr = self.run_main(inspect_backends.main, [])
    self.assertEqual((code, stderr), (0, ""))
    report = json.loads(stdout)
    self.assertFalse(report["connection_attempted"])
    self.assertFalse(report["serial_usb_network_access"])


if __name__ == "__main__":
  unittest.main()
