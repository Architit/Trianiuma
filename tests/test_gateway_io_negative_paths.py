from __future__ import annotations

import os
import subprocess
import tarfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "gateway_io.sh"


def test_gateway_io_unknown_command_exits_2():
    proc = subprocess.run(
        ["bash", str(SCRIPT), "unknown"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 2
    assert "Usage:" in proc.stdout or "Usage:" in proc.stderr


def test_gateway_io_import_without_argument_fails():
    proc = subprocess.run(
        ["bash", str(SCRIPT), "import"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 1
    out = proc.stdout + proc.stderr
    assert "missing_archive_argument" in out


def test_gateway_io_verify_fails_when_mandatory_gateways_not_configured():
    env = os.environ.copy()
    env.pop("GATEWAY_ONEDRIVE_ROOT", None)
    env.pop("GATEWAY_GWORKSPACE_ROOT", None)
    proc = subprocess.run(
        ["bash", str(SCRIPT), "verify"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1
    assert "onedrive:warn env_not_set GATEWAY_ONEDRIVE_ROOT" in out
    assert "gworkspace:warn env_not_set GATEWAY_GWORKSPACE_ROOT" in out


def test_gateway_io_import_rejects_traversal_entries(tmp_path: Path):
    payload = tmp_path / "payload.txt"
    payload.write_text("x", encoding="utf-8")
    archive = tmp_path / "unsafe.tgz"
    with tarfile.open(archive, "w:gz") as tf:
        tf.add(payload, arcname="../escape.txt")

    env = os.environ.copy()
    env["GATEWAY_IMPORT_DIR"] = str(tmp_path / "import")
    env["GATEWAY_STAGE_DIR"] = str(tmp_path / "stage")
    proc = subprocess.run(
        ["bash", str(SCRIPT), "import", str(archive)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )

    out = proc.stdout + proc.stderr
    assert proc.returncode != 0
    assert "unsafe_path traversal" in out


def test_gateway_io_import_respects_stage_dir_override(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "ok.txt").write_text("ok", encoding="utf-8")
    archive = tmp_path / "safe.tgz"
    with tarfile.open(archive, "w:gz") as tf:
        tf.add(src / "ok.txt", arcname="ok.txt")

    stage_dir = tmp_path / "custom_stage"
    import_dir = tmp_path / "custom_import"
    env = os.environ.copy()
    env["GATEWAY_IMPORT_DIR"] = str(import_dir)
    env["GATEWAY_STAGE_DIR"] = str(stage_dir)

    proc = subprocess.run(
        ["bash", str(SCRIPT), "import", str(archive)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )

    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert f"staged_at={stage_dir}" in out
    assert (stage_dir / "ok.txt").exists()
