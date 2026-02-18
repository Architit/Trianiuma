from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_AUTOSTART = REPO_ROOT / "scripts" / "aess_autostart.sh"


def _make_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR)


def test_aess_autostart_does_not_write_stamp_when_service_start_fails(tmp_path: Path):
    repo_dir = tmp_path / "repo-under-test"
    scripts_dir = repo_dir / "scripts"
    state_root = tmp_path / "state"
    scripts_dir.mkdir(parents=True)

    autostart = scripts_dir / "aess_autostart.sh"
    autostart.write_text(SOURCE_AUTOSTART.read_text(encoding="utf-8"), encoding="utf-8")
    _make_executable(autostart)

    failing_service = scripts_dir / "aess_service_start.sh"
    failing_service.write_text("#!/usr/bin/env bash\nexit 1\n", encoding="utf-8")
    _make_executable(failing_service)

    env = os.environ.copy()
    env["AESS_STATE_ROOT"] = str(state_root)
    env["AESS_REPO_COOLDOWN_SEC"] = "300"

    proc = subprocess.run(
        ["bash", str(autostart)],
        cwd=repo_dir,
        env=env,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    stamp_file = state_root / f"{repo_dir.name}.last"
    assert not stamp_file.exists()
