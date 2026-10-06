"""Synthetic, local-only behavior tests for the pydicom helper CLIs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "pydicom"
SCRIPTS = SKILL_ROOT / "scripts"
CLI_NAMES = (
    "anonymize_dicom.py",
    "deidentification_audit.py",
    "dicom_inventory.py",
    "dicom_to_image.py",
    "extract_metadata.py",
    "pixel_frame_planner.py",
    "transfer_syntax_inspector.py",
    "uid_mapping_validator.py",
)


def run_script(
    name: str, *arguments: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *map(str, arguments)],
        check=False,
        capture_output=True,
        cwd=cwd,
        env=environment,
        text=True,
        timeout=45,
    )


def require_test_stack() -> tuple[object, object]:
    try:
        import numpy
        import pydicom
    except ImportError as exc:
        raise unittest.SkipTest(
            "run with pinned pydicom and NumPy to exercise synthetic fixtures"
        ) from exc
    return pydicom, numpy


def write_fixture(
    path: Path,
    *,
    study_uid: str | None = None,
    referenced_uid: str | None = None,
    frames: int = 2,
) -> dict[str, str]:
    pydicom, numpy = require_test_stack()
    from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
    from pydicom.sequence import Sequence
    from pydicom.uid import (
        PYDICOM_IMPLEMENTATION_UID,
        ExplicitVRLittleEndian,
        SecondaryCaptureImageStorage,
        generate_uid,
    )

    study_uid = study_uid or generate_uid()
    referenced_uid = referenced_uid or generate_uid()
    sop_uid = generate_uid()
    series_uid = generate_uid()
    frame_uid = generate_uid()
    meta = FileMetaDataset()
    meta.FileMetaInformationVersion = b"\x00\x01"
    meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    meta.MediaStorageSOPInstanceUID = sop_uid
    meta.TransferSyntaxUID = ExplicitVRLittleEndian
    meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID

    dataset = FileDataset(str(path), {}, file_meta=meta, preamble=b"\0" * 128)
    dataset.SOPClassUID = SecondaryCaptureImageStorage
    dataset.SOPInstanceUID = sop_uid
    dataset.StudyInstanceUID = study_uid
    dataset.SeriesInstanceUID = series_uid
    dataset.FrameOfReferenceUID = frame_uid
    dataset.Modality = "OT"
    dataset.PatientName = "SYNTHETIC^SUBJECT"
    dataset.PatientID = "SYNTHETIC-001"
    dataset.PatientBirthDate = "20000229"
    dataset.PatientAddress = "SYNTHETIC ADDRESS"
    dataset.StudyDate = "20200102"
    dataset.StudyTime = "120102"
    dataset.AcquisitionDateTime = "20200102120102.123456-0500"
    dataset.AccessionNumber = "SYN-ACCESSION"
    dataset.StudyID = "SYNTHETIC-STUDY"
    dataset.StudyDescription = "SYNTHETIC FREE TEXT"
    dataset.InstitutionName = "SYNTHETIC INSTITUTION"
    dataset.BurnedInAnnotation = "YES"
    dataset.RecognizableVisualFeatures = "NO"
    dataset.PatientIdentityRemoved = "NO"

    dataset.Rows = 2
    dataset.Columns = 3
    dataset.SamplesPerPixel = 1
    dataset.PhotometricInterpretation = "MONOCHROME2"
    dataset.BitsAllocated = 16
    dataset.BitsStored = 12
    dataset.HighBit = 11
    dataset.PixelRepresentation = 0
    if frames > 1:
        dataset.NumberOfFrames = str(frames)
    pixels = numpy.arange(frames * 6, dtype=numpy.uint16).reshape(frames, 2, 3)
    dataset.PixelData = pixels.tobytes()

    item = Dataset()
    item.ReferencedSOPClassUID = SecondaryCaptureImageStorage
    item.ReferencedSOPInstanceUID = referenced_uid
    item.PatientName = "SYNTHETIC^NESTED"
    dataset.ReferencedImageSequence = Sequence([item])
    dataset.add_new((0x0011, 0x0010), "LO", "SYNTHETIC_CREATOR")
    dataset.add_new((0x0011, 0x1010), "LO", "SYNTHETIC PRIVATE VALUE")

    pydicom.dcmwrite(path, dataset, enforce_file_format=True, overwrite=False)
    return {
        "frame_uid": frame_uid,
        "referenced_uid": referenced_uid,
        "series_uid": series_uid,
        "sop_uid": sop_uid,
        "study_uid": study_uid,
    }


class DependencyFreeHelpTests(unittest.TestCase):
    def test_all_cli_helps_succeed_without_importing_optional_packages(self) -> None:
        for name in CLI_NAMES:
            with self.subTest(name=name):
                result = run_script(name, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout.casefold())


class SyntheticInventoryTests(unittest.TestCase):
    def test_redacted_extract_inventory_and_frame_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)

            extracted = run_script("extract_metadata.py", source.name, cwd=root)
            self.assertEqual(extracted.returncode, 0, extracted.stderr)
            self.assertNotIn("SYNTHETIC", extracted.stdout)
            extract_report = json.loads(extracted.stdout)
            self.assertTrue(extract_report["allowlist_only"])
            self.assertFalse(extract_report["phi_values_emitted"])
            self.assertEqual(extract_report["aggregate"]["successful_files"], 1)

            inventory = run_script("dicom_inventory.py", source.name, cwd=root)
            self.assertEqual(inventory.returncode, 0, inventory.stderr)
            self.assertNotIn("SYNTHETIC", inventory.stdout)
            inventory_report = json.loads(inventory.stdout)
            self.assertTrue(inventory_report["metadata_only"])
            self.assertTrue(inventory_report["records"][0]["ok"])
            self.assertEqual(inventory_report["records"][0]["image"]["frames"], 2)

            planner = run_script(
                "pixel_frame_planner.py",
                source.name,
                "--frames",
                "1",
                cwd=root,
            )
            self.assertEqual(planner.returncode, 0, planner.stderr)
            plan = json.loads(planner.stdout)
            self.assertFalse(plan["pixel_data_loaded"])
            self.assertEqual(plan["decode_plan"]["frame_indices"], [1])
            self.assertEqual(plan["decode_plan"]["one_frame_shape"], [2, 3])

    def test_metadata_only_limits_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)
            result = run_script(
                "pixel_frame_planner.py",
                source.name,
                "--max-decompressed-bytes",
                "1",
                cwd=root,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stdout)["ok"])


class PixelRenderingTests(unittest.TestCase):
    def test_frame_specific_non_diagnostic_render(self) -> None:
        try:
            from PIL import Image
        except ImportError as exc:
            raise unittest.SkipTest("run with pinned Pillow") from exc
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            output = root / "frame.png"
            write_fixture(source)
            result = run_script(
                "dicom_to_image.py",
                source.name,
                output.name,
                "--frame",
                "1",
                "--acknowledge-pixel-phi",
                cwd=root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertFalse(report["diagnostic_use"])
            self.assertEqual(report["frame"], 1)
            self.assertTrue(output.is_file())
            with Image.open(output) as image:
                self.assertEqual(image.size, (3, 2))

    def test_render_requires_phi_acknowledgement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)
            result = run_script(
                "dicom_to_image.py",
                source.name,
                "frame.png",
                cwd=root,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse((root / "frame.png").exists())


class PseudonymizationTests(unittest.TestCase):
    def test_scoped_uid_consistency_and_sensitive_map_validation(self) -> None:
        pydicom, numpy = require_test_stack()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            originals = write_fixture(source)
            key_result = run_script(
                "anonymize_dicom.py",
                "--generate-uid-key",
                "project.key",
                cwd=root,
            )
            self.assertEqual(key_result.returncode, 0, key_result.stderr)

            first = run_script(
                "anonymize_dicom.py",
                source.name,
                "derived-1.dcm",
                "--uid-key-file",
                "project.key",
                "--uid-scope",
                "synthetic-export-v1",
                "--audit-report",
                "derived-1.audit.json",
                "--uid-map-output",
                "uid-map.json",
                "--acknowledge-sensitive-map",
                cwd=root,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertNotIn("SYNTHETIC^SUBJECT", first.stdout)
            second = run_script(
                "anonymize_dicom.py",
                source.name,
                "derived-2.dcm",
                "--uid-key-file",
                "project.key",
                "--uid-scope",
                "synthetic-export-v1",
                "--audit-report",
                "derived-2.audit.json",
                cwd=root,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            third = run_script(
                "anonymize_dicom.py",
                source.name,
                "derived-3.dcm",
                "--uid-key-file",
                "project.key",
                "--uid-scope",
                "synthetic-export-v2",
                "--audit-report",
                "derived-3.audit.json",
                cwd=root,
            )
            self.assertEqual(third.returncode, 0, third.stderr)

            original = pydicom.dcmread(source)
            derived_1 = pydicom.dcmread(root / "derived-1.dcm")
            derived_2 = pydicom.dcmread(root / "derived-2.dcm")
            derived_3 = pydicom.dcmread(root / "derived-3.dcm")
            self.assertEqual(str(original.PatientName), "SYNTHETIC^SUBJECT")
            self.assertNotEqual(str(derived_1.PatientName), str(original.PatientName))
            self.assertTrue(str(derived_1.PatientName).startswith("PSEUDONYM^"))
            self.assertNotEqual(str(derived_1.PatientID), str(original.PatientID))
            self.assertEqual(
                str(derived_1.StudyInstanceUID), str(derived_2.StudyInstanceUID)
            )
            self.assertNotEqual(
                str(derived_1.StudyInstanceUID), str(derived_3.StudyInstanceUID)
            )
            self.assertNotEqual(str(derived_1.StudyInstanceUID), originals["study_uid"])
            self.assertNotEqual(
                str(derived_1.ReferencedImageSequence[0].ReferencedSOPInstanceUID),
                originals["referenced_uid"],
            )
            self.assertEqual(
                str(derived_1.file_meta.MediaStorageSOPInstanceUID),
                str(derived_1.SOPInstanceUID),
            )
            self.assertEqual(str(derived_1.PatientIdentityRemoved), "NO")
            self.assertEqual(str(derived_1.StudyDate), "")
            self.assertFalse(
                any(element.tag.is_private for element in derived_1.iterall())
            )
            numpy.testing.assert_array_equal(
                original.pixel_array, derived_1.pixel_array
            )

            validation = run_script(
                "uid_mapping_validator.py",
                "uid-map.json",
                "--uid-key-file",
                "project.key",
                "--uid-scope",
                "synthetic-export-v1",
                cwd=root,
            )
            self.assertEqual(validation.returncode, 0, validation.stderr)
            mapping_report = json.loads(validation.stdout)
            self.assertTrue(mapping_report["ok"])
            self.assertTrue(mapping_report["deterministic_mapping_verified"])
            self.assertNotIn(originals["study_uid"], validation.stdout)

    def test_in_place_output_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)
            run_script(
                "anonymize_dicom.py",
                "--generate-uid-key",
                "project.key",
                cwd=root,
            )
            before = source.read_bytes()
            result = run_script(
                "anonymize_dicom.py",
                source.name,
                source.name,
                "--uid-key-file",
                "project.key",
                "--uid-scope",
                "scope",
                "--audit-report",
                "audit.json",
                "--force",
                cwd=root,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_bytes(), before)

    @unittest.skipIf(os.name == "nt", "POSIX permission check")
    def test_permissive_uid_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)
            key = root / "project.key"
            key.write_bytes(b"k" * 32)
            key.chmod(0o644)
            result = run_script(
                "anonymize_dicom.py",
                source.name,
                "derived.dcm",
                "--uid-key-file",
                key.name,
                "--uid-scope",
                "scope",
                "--audit-report",
                "audit.json",
                cwd=root,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse((root / "derived.dcm").exists())

    def test_fixed_date_shift_preserves_dt_suffix_and_empties_standalone_time(
        self,
    ) -> None:
        pydicom, _ = require_test_stack()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)
            run_script(
                "anonymize_dicom.py",
                "--generate-uid-key",
                "project.key",
                cwd=root,
            )
            result = run_script(
                "anonymize_dicom.py",
                source.name,
                "shifted.dcm",
                "--uid-key-file",
                "project.key",
                "--uid-scope",
                "date-shift-scope",
                "--audit-report",
                "shifted.audit.json",
                "--date-policy",
                "shift",
                "--date-shift-days",
                "365",
                cwd=root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            shifted = pydicom.dcmread(root / "shifted.dcm")
            self.assertEqual(str(shifted.PatientBirthDate), "20010228")
            self.assertEqual(str(shifted.StudyDate), "20210101")
            self.assertEqual(str(shifted.StudyTime), "")
            self.assertEqual(
                str(shifted.AcquisitionDateTime),
                "20210101120102.123456-0500",
            )


class AuditAndCapabilityTests(unittest.TestCase):
    def test_deidentification_audit_never_claims_compliance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)
            result = run_script(
                "deidentification_audit.py",
                source.name,
                cwd=root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("SYNTHETIC", result.stdout)
            report = json.loads(result.stdout)
            self.assertTrue(report["not_a_compliance_determination"])
            self.assertGreater(
                report["aggregate"]["review_failure_files"],
                0,
            )
            self.assertGreater(
                report["aggregate"]["categories"]["nonempty_private_elements"],
                0,
            )

    def test_transfer_syntax_capability_inspector(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "synthetic.dcm"
            write_fixture(source)
            result = run_script(
                "transfer_syntax_inspector.py",
                "--input",
                source.name,
                cwd=root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["package_versions"]["pydicom"], "3.0.2")
            self.assertFalse(report["pixel_data_loaded"])
            self.assertEqual(
                report["input_selected_uid"],
                "1.2.840.10008.1.2.1",
            )


if __name__ == "__main__":
    unittest.main()
