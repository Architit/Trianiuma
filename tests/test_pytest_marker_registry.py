from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTEST_INI = REPO_ROOT / "pytest.ini"
BUILTIN_MARKS = {
    "filterwarnings",
    "parametrize",
    "skip",
    "skipif",
    "usefixtures",
    "xfail",
}


def _scan_roots() -> list[Path]:
    roots = [REPO_ROOT / "tests"]
    agents_root = REPO_ROOT / "agents"
    if agents_root.exists():
        roots.extend(sorted(p for p in agents_root.rglob("tests") if p.is_dir()))
    return roots


def _declared_markers() -> set[str]:
    text = PYTEST_INI.read_text(encoding="utf-8")
    markers = set()
    in_markers = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("markers"):
            in_markers = True
            continue
        if in_markers and line.startswith("    ") and ":" in line:
            markers.add(line.strip().split(":", 1)[0].strip())
            continue
        if in_markers and line and not line.startswith(" "):
            break
    return markers


def _used_custom_markers() -> set[str]:
    found = set()
    pattern = re.compile(r"pytest\.mark\.([a-zA-Z_][a-zA-Z0-9_]*)")
    for root in _scan_roots():
        if not root.exists():
            continue
        for path in root.rglob("test_*.py"):
            text = path.read_text(encoding="utf-8")
            for name in pattern.findall(text):
                if name not in BUILTIN_MARKS:
                    found.add(name)
    return found


def test_all_custom_pytest_marks_are_declared() -> None:
    used = _used_custom_markers()
    declared = _declared_markers()
    missing = sorted(used - declared)
    assert not missing, f"pytest.ini missing marker declarations: {missing}"
