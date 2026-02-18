from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCRIPTS = [
    REPO_ROOT / "scripts" / "gateway_io.sh",
    REPO_ROOT / "scripts" / "test_entrypoint.sh",
    REPO_ROOT / "scripts" / "aess_autostart.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "gateway_io.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "test_entrypoint.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "aess_autostart.sh",
]


def test_runtime_scripts_keep_strict_shell_mode() -> None:
    for script in RUNTIME_SCRIPTS:
        text = script.read_text(encoding="utf-8")
        assert "set -euo pipefail" in text, script


def test_gateway_scripts_reject_known_unsafe_patterns() -> None:
    gateway_scripts = [
        REPO_ROOT / "scripts" / "gateway_io.sh",
        REPO_ROOT / "agents" / "test-agent" / "scripts" / "gateway_io.sh",
    ]
    for script in gateway_scripts:
        text = script.read_text(encoding="utf-8")
        assert 'verify_onedrive || true' not in text, script
        assert 'verify_gworkspace || true' not in text, script
        assert 'rm -rf "$GATEWAY_STAGE_DIR"/*' not in text, script
