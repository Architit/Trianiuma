from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_gateway_access_contract_mentions_external_systems():
    text = (REPO_ROOT / "GATEWAY_ACCESS_CONTRACT.md").read_text(encoding="utf-8")
    assert "GitHub" in text
    assert "OneDrive" in text
    assert "Google Workspace" in text


def test_test_entrypoint_modes_declared():
    text = (REPO_ROOT / "scripts" / "test_entrypoint.sh").read_text(encoding="utf-8")
    assert "--all" in text
    assert "--unit-only" in text
    assert "--integration" in text
    assert "--governance" in text
    assert "--archlog" in text
    assert "--ci" in text


def test_test_entrypoint_unknown_mode_exits_2():
    proc = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "test_entrypoint.sh"), "--unknown-mode"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 2
    assert "usage:" in out.lower()
