from __future__ import annotations

import stat
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCRIPTS = [
    REPO_ROOT / "scripts" / "aess_autostart.sh",
    REPO_ROOT / "scripts" / "ecosystem_health_snapshot.sh",
    REPO_ROOT / "scripts" / "ecosystem_soak.sh",
    REPO_ROOT / "scripts" / "gateway_io.sh",
    REPO_ROOT / "scripts" / "test_entrypoint.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "aess_autostart.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "bootstrap_submodules.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "gateway_io.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "test_entrypoint.sh",
    REPO_ROOT / "agents" / "test-agent" / "LAM_Test" / "agents" / "codex-agent" / "run_tests_wsl.sh",
]


def test_runtime_scripts_are_executable_and_have_bash_shebang() -> None:
    for script in RUNTIME_SCRIPTS:
        assert script.exists(), script
        mode = script.stat().st_mode
        assert mode & stat.S_IXUSR, f"script is not executable by owner: {script}"
        first_line = script.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "#!/usr/bin/env bash", script
