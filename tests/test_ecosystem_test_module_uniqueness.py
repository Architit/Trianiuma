from __future__ import annotations

from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PATH_SEGMENTS = (
    "/agents/operator-agent/agents/test-agent/",
)


def _scan_roots() -> list[Path]:
    roots = [REPO_ROOT / "tests"]
    agents_root = REPO_ROOT / "agents"
    if agents_root.exists():
        roots.extend(sorted(p for p in agents_root.rglob("tests") if p.is_dir()))
    return roots


def test_test_module_basenames_are_unique_across_ecosystem() -> None:
    by_name: dict[str, list[str]] = defaultdict(list)
    for root in _scan_roots():
        if not root.exists():
            continue
        for path in root.rglob("test_*.py"):
            normalized = "/" + str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            if any(segment in normalized for segment in EXCLUDED_PATH_SEGMENTS):
                continue
            by_name[path.name].append(str(path.relative_to(REPO_ROOT)))

    duplicates = {name: paths for name, paths in by_name.items() if len(paths) > 1}
    assert not duplicates, f"duplicate test module basenames detected: {duplicates}"
