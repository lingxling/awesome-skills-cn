import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "autoskill"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
