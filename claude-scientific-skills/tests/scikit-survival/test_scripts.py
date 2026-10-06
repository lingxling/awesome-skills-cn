#!/usr/bin/env python3
"""Synthetic, network-free tests for the scikit-survival helper CLIs."""

from __future__ import annotations

import ast
import json
import stat
import sys
import tempfile
import unittest

import pytest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "scikit-survival"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

# Guarded so a bare project-environment run skips cleanly instead of failing
# collection; the real run is `tests/run_all.py --isolated scikit-survival`.
pytest.importorskip("sksurv", reason="scikit-survival needs scikit-survival")

import _common  # noqa: E402
import competing_risk_cif  # noqa: E402
import evaluate_survival_metrics  # noqa: E402
import model_report  # noqa: E402
import train_survival_model  # noqa: E402
import validate_survival_csv  # noqa: E402


class CommonSafetyTests(unittest.TestCase):
    def test_json_output_is_private_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "summary.json"
            _common.emit_json({"ok": True}, output=output)
            self.assertEqual(json.loads(output.read_text()), {"ok": True})
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            with self.assertRaises(_common.CliError):
                _common.emit_json({"ok": False}, output=output)

    def test_local_paths_reject_urls_and_symlinks(self) -> None:
        with self.assertRaises(_common.CliError):
            _common.checked_input_file(
                "https://example.invalid/data.csv", suffixes={".csv"}
            )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "data.csv"
            real.write_text("event,time\n1,2\n", encoding="utf-8")
            link = root / "link.csv"
            try:
                link.symlink_to(real)
            except OSError:
                self.skipTest("symlinks unavailable")
            with self.assertRaises(_common.CliError):
                _common.checked_input_file(link, suffixes={".csv"})

    def test_no_shadow_modules_network_or_environment_reads(self) -> None:
        filenames = {path.name for path in SCRIPTS.glob("*.py")}
        self.assertNotIn("sklearn.py", filenames)
        self.assertNotIn("sksurv.py", filenames)
        self.assertNotIn("numpy.py", filenames)
        self.assertNotIn("pandas.py", filenames)
        banned_imports = {"aiohttp", "httpx", "requests", "socket", "urllib"}
        for path in SCRIPTS.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots = {alias.name.split(".", 1)[0] for alias in node.names}
                    self.assertFalse(roots & banned_imports, path.name)
                if isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotIn(
                        node.module.split(".", 1)[0], banned_imports, path.name
                    )
                if isinstance(node, ast.Attribute):
                    self.assertFalse(
                        isinstance(node.value, ast.Name)
                        and node.value.id == "os"
                        and node.attr in {"environ", "getenv"},
                        path.name,
                    )

    def test_help_is_available_without_running_workflows(self) -> None:
        modules = (
            validate_survival_csv,
            train_survival_model,
            evaluate_survival_metrics,
            competing_risk_cif,
            model_report,
        )
        for module in modules:
            with self.subTest(module=module.__name__):
                help_text = module.build_parser().format_help()
                self.assertIn("usage:", help_text)
                self.assertIn("--help", help_text)


class ValidationTests(unittest.TestCase):
    def test_synthetic_csv_schema_converts_to_structured_array(self) -> None:
        frame, numeric, categorical = _common.synthetic_survival_frame(rows=120)
        outcome, report = validate_survival_csv.validate_and_convert(
            frame,
            event_column="event",
            time_column="time",
            feature_columns=numeric + categorical,
        )
        self.assertEqual(outcome.dtype.names, ("event", "time"))
        self.assertEqual(len(outcome), 120)
        self.assertTrue(report["validation"]["valid"])

    def test_outcome_feature_leakage_is_rejected(self) -> None:
        frame, _, _ = _common.synthetic_survival_frame(rows=80)
        with self.assertRaises(_common.CliError):
            validate_survival_csv.validate_and_convert(
                frame,
                event_column="event",
                time_column="time",
                feature_columns=["event", "x_linear"],
            )

    def test_structured_output_disables_pickle(self) -> None:
        import numpy as np

        frame, _, _ = _common.synthetic_survival_frame(rows=80)
        outcome, _ = validate_survival_csv.validate_and_convert(
            frame,
            event_column="event",
            time_column="time",
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "outcome.npy"
            _common.atomic_save_npy(outcome, output)
            restored = np.load(output, allow_pickle=False)
        self.assertEqual(restored.dtype.names, ("event", "time"))


class TrainingTests(unittest.TestCase):
    def test_cox_pipeline_splits_before_learned_preprocessing(self) -> None:
        frame, numeric, categorical = _common.synthetic_survival_frame(rows=140)
        estimator, train_data, test_data, report = (
            train_survival_model.train_and_report(
                frame,
                event_column="event",
                time_column="time",
                numeric_columns=numeric,
                categorical_columns=categorical,
                model_name="coxph",
                test_fraction=0.25,
                seed=_common.DEFAULT_SEED,
                tune=False,
                outer_folds=2,
                inner_folds=2,
            )
        )
        self.assertTrue(
            report["leakage_controls"]["split_before_imputation_encoding_scaling"]
        )
        self.assertEqual(report["data"]["rows_train"], 105)
        self.assertEqual(report["data"]["rows_test"], 35)
        self.assertEqual(
            estimator.named_steps["model"].__class__.__name__, "CoxPHSurvivalAnalysis"
        )
        self.assertEqual(len(train_data[1]), 105)
        self.assertEqual(len(test_data[1]), 35)

    def test_nested_tuning_runs_inside_training_data(self) -> None:
        frame, numeric, categorical = _common.synthetic_survival_frame(rows=120)
        _, _, _, report = train_survival_model.train_and_report(
            frame,
            event_column="event",
            time_column="time",
            numeric_columns=numeric,
            categorical_columns=categorical,
            model_name="coxph",
            test_fraction=0.25,
            seed=17,
            tune=True,
            outer_folds=2,
            inner_folds=2,
        )
        self.assertTrue(report["tuning"]["performed"])
        self.assertEqual(len(report["tuning"]["outer_results"]), 2)
        self.assertFalse(report["leakage_controls"]["holdout_used_for_tuning"])

    def test_explicit_schema_is_required(self) -> None:
        frame, _, _ = _common.synthetic_survival_frame(rows=80)
        with self.assertRaises(_common.CliError):
            train_survival_model.resolve_schema(
                frame,
                event_column="event",
                time_column="time",
                numeric_columns=[],
                categorical_columns=[],
            )


class MetricTests(unittest.TestCase):
    def test_synthetic_metrics_cover_risk_and_probability_inputs(self) -> None:
        report = evaluate_survival_metrics.evaluate(
            evaluate_survival_metrics.synthetic_metric_inputs()
        )
        metrics = report["metrics"]
        self.assertIsInstance(metrics["harrell_c"], float)
        self.assertIsInstance(metrics["uno_c"], float)
        self.assertIsInstance(metrics["integrated_brier_score"], float)
        self.assertEqual(len(metrics["cumulative_dynamic_auc"]["values"]), 8)

    def test_risk_and_survival_shapes_are_distinct(self) -> None:
        arrays = evaluate_survival_metrics.synthetic_metric_inputs()
        arrays["survival"] = arrays["risk"]
        with self.assertRaises(_common.CliError):
            evaluate_survival_metrics.validate_predictions(arrays)

    def test_time_grid_outside_training_support_is_rejected(self) -> None:
        arrays = evaluate_survival_metrics.synthetic_metric_inputs()
        arrays["test_time"] = arrays["test_time"].copy()
        arrays["test_time"][0] = arrays["train_time"].max() + 1
        with self.assertRaises(_common.CliError):
            evaluate_survival_metrics.validate_predictions(arrays)


class CompetingRiskTests(unittest.TestCase):
    def test_cif_shapes_and_sum_identity(self) -> None:
        import numpy as np

        frame, _ = competing_risk_cif.synthetic_competing_risks(rows=160)
        summary, arrays = competing_risk_cif.estimate_cif(
            frame["status"],
            frame["time"],
            confidence=True,
        )
        cif = arrays["cumulative_incidence"]
        self.assertEqual(summary["n_causes"], 3)
        self.assertEqual(cif.shape[0], 4)
        self.assertTrue(np.allclose(cif[0], cif[1:].sum(axis=0)))
        self.assertEqual(arrays["confidence_interval"].shape[:2], (4, 2))

    def test_noncontiguous_cause_codes_are_rejected(self) -> None:
        with self.assertRaises(_common.CliError):
            competing_risk_cif.normalize_competing_event([0, 1, 3, 1, 3])


class ReportTests(unittest.TestCase):
    def test_report_distinguishes_metrics_and_disclaims_utility(self) -> None:
        report = model_report.render_report(
            model_report.synthetic_training_summary(),
            model_report.synthetic_metric_summary(),
            competing_risks="present",
            title="Synthetic survival report",
        )
        self.assertIn("rank discrimination", report)
        self.assertIn("probability prediction error", report)
        self.assertIn("cause-specific CIF", report)
        self.assertIn("not clinical advice", report)


if __name__ == "__main__":
    unittest.main()
