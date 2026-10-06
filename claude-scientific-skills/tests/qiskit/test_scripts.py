"""Tests for the Qiskit environment, primitive, and backend-inspection scripts.

Three failure modes are worth guarding here. First, `run_local_primitives`
claims a specific piece of quantum mechanics: `ry(theta)` then `cx` prepares
cos(theta/2)|00> + sin(theta/2)|11>, so the sampler must only ever see `00` and
`11`, and the estimator of `1.0*ZI + 0.5*XX` must return cos(theta) +
0.5*sin(theta). Those are values known before the code runs, and at
theta = pi/2 the state is the Bell state, whose measurement distribution is
textbook. Second, `check_environment` is the script an agent trusts to decide
whether the environment is usable, so both directions matter -- a healthy
install must report `ok`, and a version drift must land in `warnings` normally
but in `errors` under `--strict`. Third, `inspect_runtime` promises to read a
backend and never submit a job; it is checked against a fake five-qubit linear
device, whose coupling map and gate set are known by construction.
"""

from __future__ import annotations

import json
import math
import sys
import unittest
from importlib import metadata
from pathlib import Path

import pytest

import skill_contract

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "qiskit"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

pytest.importorskip("qiskit", reason="qiskit scripts need qiskit")
pytest.importorskip("numpy", reason="qiskit scripts need numpy")

import check_environment  # noqa: E402
import inspect_runtime  # noqa: E402
import run_local_primitives  # noqa: E402

CliHelpTests = skill_contract.cli.help_test_case(SKILL_ROOT)


def installed(distribution: str) -> str | None:
    """The installed version, read independently of the script under test."""
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


class ImportProbeTests(unittest.TestCase):
    def test_a_distribution_that_is_not_installed_has_no_version(self) -> None:
        self.assertIsNone(check_environment.installed_version("no-such-distribution"))

    def test_an_installed_distribution_reports_its_version(self) -> None:
        self.assertEqual(check_environment.installed_version("qiskit"), installed("qiskit"))

    def test_a_missing_module_is_reported_with_the_import_error(self) -> None:
        status = check_environment.import_status("no_such_module_at_all")
        self.assertFalse(status["ok"])
        self.assertIsNone(status["module_file"])
        self.assertIn("ModuleNotFoundError", status["error"])

    def test_an_importable_module_reports_where_it_came_from(self) -> None:
        # The module file is what distinguishes "installed" from "importable":
        # a broken optional environment must be nameable, not just falsy.
        status = check_environment.import_status("qiskit")
        self.assertTrue(status["ok"])
        self.assertIsNone(status["error"])
        self.assertTrue(status["module_file"].endswith("__init__.py"))


class EnvironmentReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.report, self.errors, self.warnings = check_environment.collect_report(
            require_runtime=False, require_aer=False, strict=False
        )

    def test_qiskit_alone_is_required_by_default(self) -> None:
        required = {
            name
            for name, details in self.report["packages"].items()
            if details["required"]
        }
        self.assertEqual(required, {"qiskit"})

    def test_the_optional_extras_become_required_on_request(self) -> None:
        report, _, _ = check_environment.collect_report(
            require_runtime=True, require_aer=True, strict=False
        )
        required = {
            name for name, details in report["packages"].items() if details["required"]
        }
        self.assertEqual(required, {"qiskit", "qiskit-ibm-runtime", "qiskit-aer"})

    def test_the_core_api_smoke_check_passes_on_a_working_install(self) -> None:
        # This is the whole point of the script: the imports it exercises are
        # the ones every documented workflow starts from.
        self.assertTrue(self.report["core_api_smoke_check"]["ok"])
        self.assertIsNone(self.report["core_api_smoke_check"]["error"])

    def test_ok_is_exactly_the_absence_of_errors(self) -> None:
        # main() turns this into the process exit code.
        self.assertEqual(self.report["ok"], not self.errors)

    def test_a_healthy_environment_reports_no_errors(self) -> None:
        self.assertEqual(self.errors, [])

    def test_installed_versions_are_read_from_the_metadata(self) -> None:
        for name, details in self.report["packages"].items():
            with self.subTest(distribution=name):
                self.assertEqual(details["installed_version"], installed(name))

    def test_version_drift_is_a_warning_but_an_error_under_strict(self) -> None:
        # Expectations are derived from importlib.metadata and the script's own
        # published baseline, not from the report being checked.
        drifted = {
            name: (installed(name), verified)
            for name, verified in check_environment.VERIFIED_VERSIONS.items()
            if installed(name) is not None and installed(name) != verified
        }
        strict_report, strict_errors, strict_warnings = check_environment.collect_report(
            require_runtime=True, require_aer=True, strict=True
        )
        for name, (current, verified) in drifted.items():
            message = (
                f"{name}=={current} differs from the verified baseline {verified}."
            )
            with self.subTest(distribution=name):
                self.assertFalse(
                    self.report["packages"][name]["version_matches_verified"]
                )
                self.assertIn(message, self.warnings)
                self.assertNotIn(message, self.errors)
                if name in {"qiskit", "qiskit-ibm-runtime", "qiskit-aer"}:
                    self.assertIn(message, strict_errors)
                    self.assertNotIn(message, strict_warnings)
        for name, verified in check_environment.VERIFIED_VERSIONS.items():
            if name not in drifted and installed(name) is not None:
                with self.subTest(distribution=name, drift=False):
                    self.assertTrue(
                        self.report["packages"][name]["version_matches_verified"]
                    )
                    self.assertFalse(
                        any(name in warning for warning in strict_warnings)
                    )

    def test_a_clean_namespace_reports_no_legacy_terra(self) -> None:
        # Mixing qiskit-terra with qiskit 2.x is unrecoverable, so the script
        # must say so; with no terra installed the field stays empty.
        self.assertIsNone(installed("qiskit-terra"))
        self.assertIsNone(self.report["legacy_qiskit_terra"])
        self.assertFalse(any("terra" in error for error in self.errors))

    def test_the_report_survives_json_serialisation(self) -> None:
        # --json is the machine-readable contract, so every value has to be
        # JSON-safe; an exception object smuggled into it would break it.
        round_tripped = json.loads(json.dumps(self.report, sort_keys=True))
        self.assertEqual(round_tripped["packages"].keys(), self.report["packages"].keys())


class ShotAndAngleValidationTests(unittest.TestCase):
    def test_a_shot_count_inside_the_documented_range_is_accepted(self) -> None:
        self.assertEqual(run_local_primitives.positive_bounded_shots("1"), 1)
        self.assertEqual(
            run_local_primitives.positive_bounded_shots(str(run_local_primitives.MAX_SHOTS)),
            run_local_primitives.MAX_SHOTS,
        )

    def test_shot_counts_outside_the_range_are_rejected(self) -> None:
        import argparse

        for value in ("0", "-1", str(run_local_primitives.MAX_SHOTS + 1)):
            with self.subTest(shots=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    run_local_primitives.positive_bounded_shots(value)

    def test_a_finite_angle_is_accepted_and_an_infinite_one_is_not(self) -> None:
        import argparse

        self.assertEqual(run_local_primitives.finite_float("-0.5"), -0.5)
        for value in ("inf", "-inf", "nan"):
            with self.subTest(theta=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    run_local_primitives.finite_float(value)


class LocalPrimitiveWorkflowTests(unittest.TestCase):
    def test_at_theta_pi_over_two_the_circuit_is_a_bell_state(self) -> None:
        # ry(pi/2) then cx prepares (|00> + |11>)/sqrt(2). No other basis state
        # has any amplitude, so no other bitstring can ever be sampled.
        result = run_local_primitives.run_workflow(shots=2048, seed=11, theta_value=math.pi / 2)
        self.assertEqual(set(result["sampler"]["counts"]), {"00", "11"})

    def test_the_estimator_reproduces_the_analytic_expectation(self) -> None:
        # <ZI> = cos(theta) and <XX> = sin(theta) for that state, so the
        # observable 1.0*ZI + 0.5*XX has expectation cos + 0.5*sin exactly.
        for theta in (0.0, 0.7, math.pi / 2, math.pi):
            with self.subTest(theta=theta):
                result = run_local_primitives.run_workflow(
                    shots=64, seed=3, theta_value=theta
                )
                estimator = result["estimator"]
                self.assertAlmostEqual(
                    estimator["expectation_value"],
                    math.cos(theta) + 0.5 * math.sin(theta),
                    places=10,
                )
                self.assertAlmostEqual(
                    estimator["analytic_expectation"],
                    math.cos(theta) + 0.5 * math.sin(theta),
                    places=12,
                )
                self.assertLess(estimator["absolute_error"], 1e-9)

    def test_a_zero_angle_leaves_both_qubits_in_the_ground_state(self) -> None:
        result = run_local_primitives.run_workflow(shots=256, seed=5, theta_value=0.0)
        self.assertEqual(result["sampler"]["counts"], {"00": 256})
        self.assertEqual(result["sampler"]["probabilities"], {"00": 1.0})
        self.assertAlmostEqual(result["estimator"]["expectation_value"], 1.0, places=12)

    def test_a_pi_angle_flips_both_qubits(self) -> None:
        # ry(pi)|0> = |1> up to sign, and cx then flips the second qubit.
        result = run_local_primitives.run_workflow(shots=256, seed=5, theta_value=math.pi)
        self.assertEqual(result["sampler"]["counts"], {"11": 256})
        self.assertAlmostEqual(result["estimator"]["expectation_value"], -1.0, places=12)

    def test_every_requested_shot_is_accounted_for(self) -> None:
        result = run_local_primitives.run_workflow(shots=777, seed=2, theta_value=1.0)
        self.assertEqual(sum(result["sampler"]["counts"].values()), 777)
        self.assertAlmostEqual(sum(result["sampler"]["probabilities"].values()), 1.0)

    def test_the_sampled_frequencies_match_the_analytic_probabilities(self) -> None:
        theta = 1.0
        result = run_local_primitives.run_workflow(shots=20000, seed=7, theta_value=theta)
        expected = result["sampler"]["expected_probabilities"]
        self.assertAlmostEqual(expected["00"], math.cos(theta / 2) ** 2, places=12)
        self.assertAlmostEqual(expected["11"], math.sin(theta / 2) ** 2, places=12)
        for bitstring, probability in result["sampler"]["probabilities"].items():
            with self.subTest(bitstring=bitstring):
                # 20k shots: three standard errors is under 0.011.
                self.assertAlmostEqual(probability, expected[bitstring], delta=0.02)

    def test_the_same_seed_reproduces_the_same_counts(self) -> None:
        first = run_local_primitives.run_workflow(shots=512, seed=42, theta_value=0.9)
        second = run_local_primitives.run_workflow(shots=512, seed=42, theta_value=0.9)
        self.assertEqual(first["sampler"]["counts"], second["sampler"]["counts"])

    def test_the_reported_parameter_order_is_the_circuit_binding_order(self) -> None:
        # Values are bound positionally, so a wrong order silently runs the
        # wrong circuit.
        result = run_local_primitives.run_workflow(shots=16, seed=1, theta_value=0.3)
        self.assertEqual(result["parameter_order"], ["theta"])
        self.assertEqual(result["theta"], 0.3)


class QubitCountValidationTests(unittest.TestCase):
    def test_a_plausible_qubit_floor_is_accepted(self) -> None:
        self.assertEqual(inspect_runtime.positive_qubits("5"), 5)
        self.assertEqual(inspect_runtime.positive_qubits("10000"), 10_000)

    def test_an_implausible_qubit_floor_is_rejected(self) -> None:
        import argparse

        for value in ("0", "-3", "10001"):
            with self.subTest(qubits=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    inspect_runtime.positive_qubits(value)

    def test_an_absent_distribution_reports_no_version(self) -> None:
        self.assertIsNone(inspect_runtime.distribution_version("no-such-distribution"))
        self.assertEqual(
            inspect_runtime.distribution_version("qiskit"), installed("qiskit")
        )


class RecordingService:
    """A stand-in for QiskitRuntimeService that records how it was called."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def backend(self, name, **kwargs):
        self.calls.append(("backend", {"name": name, **kwargs}))
        return f"named:{name}"

    def least_busy(self, **kwargs):
        self.calls.append(("least_busy", kwargs))
        return "least_busy"


class BackendSelectionTests(unittest.TestCase):
    def test_a_named_backend_is_fetched_by_name(self) -> None:
        service = RecordingService()
        selected = inspect_runtime.select_backend(
            service, "ibm_torino", min_qubits=5, use_fractional_gates=None
        )
        self.assertEqual(selected, "named:ibm_torino")
        self.assertEqual(service.calls, [("backend", {"name": "ibm_torino"})])

    def test_without_a_name_the_least_busy_real_device_is_selected(self) -> None:
        service = RecordingService()
        selected = inspect_runtime.select_backend(
            service, None, min_qubits=27, use_fractional_gates=None
        )
        self.assertEqual(selected, "least_busy")
        self.assertEqual(
            service.calls,
            [
                (
                    "least_busy",
                    {"operational": True, "simulator": False, "min_num_qubits": 27},
                )
            ],
        )

    def test_the_fractional_gate_flag_is_forwarded_only_when_it_is_set(self) -> None:
        # None must mean "use the service default", not "disable" -- passing
        # use_fractional_gates=False changes which target you get back.
        for requested in (True, False):
            with self.subTest(fractional=requested):
                service = RecordingService()
                inspect_runtime.select_backend(
                    service, "ibm_torino", min_qubits=5, use_fractional_gates=requested
                )
                self.assertEqual(
                    service.calls[0][1],
                    {"name": "ibm_torino", "use_fractional_gates": requested},
                )


class BackendInspectionTests(unittest.TestCase):
    """Checked against a fake device whose topology is known by construction."""

    @classmethod
    def setUpClass(cls) -> None:
        fake_provider = pytest.importorskip(
            "qiskit_ibm_runtime.fake_provider",
            reason="inspect_runtime needs qiskit-ibm-runtime",
        )
        cls.backend = fake_provider.FakeManilaV2()
        cls.report = inspect_runtime.inspect_backend(cls.backend)

    def test_inspecting_a_backend_submits_no_jobs(self) -> None:
        # The script's central promise: it reads a target, it never queues work.
        self.assertEqual(self.report["submitted_jobs"], 0)

    def test_the_backend_identity_is_reported(self) -> None:
        self.assertEqual(self.report["backend"]["name"], "fake_manila")
        self.assertEqual(self.report["backend"]["num_qubits"], 5)

    def test_a_five_qubit_line_has_eight_directed_coupling_edges(self) -> None:
        # Manila is a linear chain 0-1-2-3-4: four links, both directions.
        self.assertEqual(self.report["target"]["coupling_edge_count"], 8)
        edges = {tuple(edge) for edge in self.report["target"]["coupling_edges"]}
        self.assertEqual(
            edges,
            {(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)},
        )

    def test_the_reported_basis_gates_are_the_targets_own(self) -> None:
        self.assertEqual(
            self.report["target"]["operation_names"],
            sorted(self.backend.operation_names),
        )

    def test_control_flow_support_is_reported_from_the_target(self) -> None:
        exposed = set(self.report["target"]["control_flow_operations"])
        self.assertLessEqual(exposed, {"if_else", "while_loop", "for_loop", "switch_case", "store"})
        self.assertEqual(exposed, {"for_loop", "if_else", "switch_case"} & set(self.backend.operation_names))

    def test_fractional_gates_are_not_claimed_on_a_backend_without_them(self) -> None:
        # Manila's basis is rz/sx/x/cx, so neither rx nor rzz is present and the
        # report must not advertise fractional-gate support.
        self.assertNotIn("rx", self.backend.operation_names)
        self.assertEqual(self.report["target"]["fractional_gate_candidates"], [])

    def test_the_report_survives_json_serialisation(self) -> None:
        round_tripped = json.loads(json.dumps(self.report, sort_keys=True))
        self.assertEqual(round_tripped["backend"]["num_qubits"], 5)


if __name__ == "__main__":
    unittest.main()
