from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "ecosystem_soak.sh"


def test_soak_script_emits_json_summary_for_single_iteration() -> None:
    env = os.environ.copy()
    env["SOAK_TEST_ARGS"] = "tests/test_runtime_smoke.py"
    proc = subprocess.run(
        ["bash", str(SCRIPT), "1"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["iterations"] == 1
    assert payload["status"] == "ok"
    assert payload["exit_code"] == 0
    assert payload["repo_root"] == str(REPO_ROOT)
    assert re.fullmatch(r"\d+ passed in .+", payload["last_summary"])
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", payload["ts_utc"])


def test_soak_script_rejects_invalid_iterations_argument() -> None:
    proc = subprocess.run(
        ["bash", str(SCRIPT), "0"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    assert proc.returncode == 2
    assert "usage:" in proc.stderr.lower()


def test_soak_script_rejects_non_numeric_iterations_argument() -> None:
    proc = subprocess.run(
        ["bash", str(SCRIPT), "abc"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    assert proc.returncode == 2
    assert "usage:" in proc.stderr.lower()


def test_soak_script_emits_failure_json_when_pytest_fails() -> None:
    env = os.environ.copy()
    env["SOAK_TEST_ARGS"] = "tests/does_not_exist"
    proc = subprocess.run(
        ["bash", str(SCRIPT), "1"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
        check=False,
    )
    assert proc.returncode != 0
    payload = json.loads(proc.stdout)
    assert payload["status"] == "fail"
    assert payload["exit_code"] != 0
    assert payload["iterations"] == 1
    assert payload["repo_root"] == str(REPO_ROOT)
    assert payload["last_summary"]


def test_soak_script_cleans_up_tmp_logs() -> None:
    env = os.environ.copy()
    env["SOAK_TEST_ARGS"] = "tests/test_runtime_smoke.py"
    env["SOAK_LOG_PREFIX"] = f"ecosystem_soak_contract_cleanup_{os.getpid()}"
    pattern = f"{env['SOAK_LOG_PREFIX']}_*.log"
    before = {p.name for p in Path("/tmp").glob(pattern)}
    proc = subprocess.run(
        ["bash", str(SCRIPT), "1"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    after = {p.name for p in Path("/tmp").glob(pattern)}
    assert after - before == set()


def test_soak_script_does_not_require_hardcoded_python3_for_json_encoding() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert 'python3 -c \'import json,sys; print(json.dumps(sys.stdin.read()))\'' not in text
    assert '"$PYTHON_BIN" -c \'import json,sys; print(json.dumps(sys.stdin.read()))\'' in text
