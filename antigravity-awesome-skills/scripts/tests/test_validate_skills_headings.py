import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from validate_skills import has_when_to_use_section

SAMPLES = [
    ("## When to Use", True),
    ("## Use this skill when", True),
    ("## When to Use This Skill", True),
    ("## Overview", False),
]

for heading, expected in SAMPLES:
    content = f"\n{heading}\n- item\n"
    assert has_when_to_use_section(content) is expected, heading

print("ok")
