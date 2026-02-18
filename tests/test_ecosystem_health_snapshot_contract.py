from __future__ import annotations

import json
import re
import stat
import subprocess
from pathlib import Path

from test_script_runtime_contracts import RUNTIME_SCRIPTS


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "ecosystem_health_snapshot.sh"


def test_snapshot_script_is_executable() -> None:
    mode = SCRIPT.stat().st_mode
    assert mode & stat.S_IXUSR


def test_snapshot_script_emits_expected_json_shape() -> None:
    proc = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)

    assert "ts_utc" in payload
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", payload["ts_utc"])
    assert "repo_root" in payload
    assert payload["repo_root"] == str(REPO_ROOT)
    assert "runtime_scripts" in payload
    expected_runtime = {str(path.relative_to(REPO_ROOT)) for path in RUNTIME_SCRIPTS}
    actual_runtime = set(payload["runtime_scripts"])
    assert actual_runtime == expected_runtime
    for rel in payload["runtime_scripts"]:
        path = REPO_ROOT / rel
        assert path.exists(), rel
        mode = path.stat().st_mode
        assert mode & stat.S_IXUSR, rel
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "#!/usr/bin/env bash", rel
    assert "test_inventory" in payload
    inv = payload["test_inventory"]
    assert "total_test_files" in inv
    assert "root_tests" in inv
    assert "operator_agent_tests" in inv
    assert "test_agent_tests" in inv
    assert "lam_nested_agent_tests" in inv


def test_snapshot_script_reports_recursive_test_inventory() -> None:
    proc = subprocess.run(
        ["bash", str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    inv = payload["test_inventory"]

    expected_total = len(
        [
            p
            for p in REPO_ROOT.rglob("test_*.py")
            if "/tests/" in str(p).replace("\\", "/")
        ]
    )
    expected_root = len(list((REPO_ROOT / "tests").rglob("test_*.py")))
    expected_operator = len(list((REPO_ROOT / "agents" / "operator-agent" / "tests").rglob("test_*.py")))
    expected_test_agent = len(list((REPO_ROOT / "agents" / "test-agent" / "tests").rglob("test_*.py")))
    nested_root = REPO_ROOT / "agents" / "test-agent" / "LAM_Test" / "agents"
    expected_nested = len(
        [
            p
            for p in nested_root.rglob("test_*.py")
            if "/tests/" in str(p).replace("\\", "/")
        ]
    )

    assert inv["total_test_files"] == expected_total
    assert inv["root_tests"] == expected_root
    assert inv["operator_agent_tests"] == expected_operator
    assert inv["test_agent_tests"] == expected_test_agent
    assert inv["lam_nested_agent_tests"] == expected_nested


def test_snapshot_script_works_when_nested_agent_tree_is_missing(tmp_path: Path) -> None:
    # Run a copied script in a minimal synthetic workspace where optional
    # nested agent folders are absent; snapshot should still emit valid JSON.
    script_dir = tmp_path / "scripts"
    script_dir.mkdir(parents=True)
    copied = script_dir / "ecosystem_health_snapshot.sh"
    copied.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")

    proc = subprocess.run(
        ["bash", str(copied)],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    inv = payload["test_inventory"]
    assert inv["lam_nested_agent_tests"] == 0
