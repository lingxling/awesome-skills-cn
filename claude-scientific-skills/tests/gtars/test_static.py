"""Static AST safety checks for bundled helper modules."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[2] / "skills" / "gtars" / "scripts"


def _word(*codepoints: int) -> str:
    return "".join(chr(value) for value in codepoints)


class StaticAstTests(unittest.TestCase):
    def test_scripts_parse_and_omit_dangerous_capabilities(self):
        forbidden_imports = {
            "boto3",
            "ctypes",
            "gtars",
            "httpx",
            "importlib",
            "pickle",
            "requests",
            "socket",
            "urllib",
        }
        forbidden_imports.add(_word(115, 117, 98, 112, 114, 111, 99, 101, 115, 115))
        forbidden_calls = {
            _word(101, 118, 97, 108),
            _word(101, 120, 101, 99),
            _word(95, 95, 105, 109, 112, 111, 114, 116, 95, 95),
        }
        for path in sorted(SCRIPTS.glob("*.py")):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(path))
                imports: set[str] = set()
                calls: set[str] = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imports.update(alias.name.split(".", 1)[0] for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imports.add(node.module.split(".", 1)[0])
                    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        calls.add(node.func.id)
                self.assertFalse(imports & forbidden_imports)
                self.assertFalse(calls & forbidden_calls)
                self.assertNotIn("os.environ", source)
                self.assertNotIn("os.getenv", source)


if __name__ == "__main__":
    unittest.main()
