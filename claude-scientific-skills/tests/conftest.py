"""Session guard for the repo-wide test tree.

Every skill's `scripts/` directory is self-contained and owns plain top-level
module names -- 32 skills ship a `scripts/_common.py`, and names like
`cluster.py` or `validate_manifest.py` are shared too. Tests import those
scripts by putting the skill's `scripts/` directory on `sys.path`, so two
skills collected into one interpreter would resolve `_common` to whichever
skill was imported first and silently test the wrong files.

Each skill therefore gets its own process:

    pytest tests/<skill>          # one skill
    python tests/run_all.py       # every skill, one process each

This module also installs `tests/_contract/` as the importable module
`skill_contract` -- the assertions every skill shares, factored out of the
per-skill suites. See `_install_contract` for why it is loaded by file
location rather than by putting `tests/` on `sys.path`.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

# Several suites assert that a skill directory ships no .pyc files. Importing
# and subprocessing the skill's scripts is what creates them, so keep the
# interpreter -- and any child it spawns -- from writing bytecode at all.
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

TESTS_DIR = Path(__file__).resolve().parent


def _install_contract() -> None:
    """Make the shared contract importable as `skill_contract`.

    `tests/` must never go on `sys.path`: in prepend/append import mode that
    turns every `tests/<skill>/` directory into an importable namespace
    package, so `tests/simpy/`, `tests/qutip/` and `tests/neurokit2/` would
    shadow the real libraries (see `addopts` in pyproject.toml). Loading the
    package by file location and registering it under a name no skill uses
    gives suites `import skill_contract` without that hazard.
    """
    if "skill_contract" in sys.modules:
        return
    package = TESTS_DIR / "_contract"
    spec = importlib.util.spec_from_file_location(
        "skill_contract",
        package / "__init__.py",
        submodule_search_locations=[str(package)],
    )
    module = importlib.util.module_from_spec(spec)
    # Registered before exec_module so the package's own `from . import cli`
    # resolves against the name suites will use.
    sys.modules["skill_contract"] = module
    spec.loader.exec_module(module)


_install_contract()


def _skill_dirs(config: pytest.Config) -> set[str]:
    """Return the names of the skill directories this session would collect.

    Underscore-prefixed directories are infrastructure, not skills:
    `_contract/` is a library and `_meta/` runs the repo-wide contract without
    importing any skill code, so neither participates in the one-skill-per-
    process rule.
    """
    everything = {
        path.name
        for path in TESTS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith((".", "_"))
    }
    selected: set[str] = set()
    for argument in config.args:
        path = Path(str(argument).split("::")[0])
        if not path.is_absolute():
            path = Path(config.invocation_params.dir) / path
        try:
            relative = path.resolve().relative_to(TESTS_DIR)
        except ValueError:
            continue
        if relative.parts:
            selected.add(relative.parts[0])
        else:
            selected |= everything
    return selected & everything


def pytest_sessionstart(session: pytest.Session) -> None:
    skills = _skill_dirs(session.config)
    if len(skills) > 1:
        raise pytest.UsageError(
            f"cannot collect {len(skills)} skills in one process: their scripts/ "
            "directories share module names (_common.py and friends), so imports "
            "would resolve to the wrong skill. Run one skill at a time with "
            "`pytest tests/<skill>`, or the whole tree with "
            "`python tests/run_all.py`."
        )
