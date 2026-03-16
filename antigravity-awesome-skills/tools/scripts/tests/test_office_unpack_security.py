import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def load_module(relative_path: str, module_name: str):
    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OfficeUnpackSecurityTests(unittest.TestCase):
    def test_extract_archive_safely_blocks_zip_slip(self):
        module = load_module("skills/docx/ooxml/scripts/unpack.py", "docx_unpack")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / "payload.zip"
            output_dir = temp_path / "output"

            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../escape.txt", "escape")
                archive.writestr("word/document.xml", "<w:document/>")

            with self.assertRaises(ValueError):
                module.extract_archive_safely(archive_path, output_dir)

            self.assertFalse((temp_path / "escape.txt").exists())


if __name__ == "__main__":
    unittest.main()
