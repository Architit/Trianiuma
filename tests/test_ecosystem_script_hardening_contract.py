from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

GATEWAY_SCRIPTS = [
    REPO_ROOT / "scripts" / "gateway_io.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "gateway_io.sh",
]

ENTRYPOINT_SCRIPTS = [
    REPO_ROOT / "scripts" / "test_entrypoint.sh",
    REPO_ROOT / "agents" / "test-agent" / "scripts" / "test_entrypoint.sh",
]


def test_gateway_scripts_keep_archive_hardening_contract() -> None:
    for script in GATEWAY_SCRIPTS:
        text = script.read_text(encoding="utf-8")
        assert "validate_archive_paths" in text, script
        assert "--no-same-owner" in text, script
        assert "--no-same-permissions" in text, script
        assert 'find "$GATEWAY_STAGE_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +' in text, script
        assert 'GATEWAY_STAGE_DIR="${GATEWAY_STAGE_DIR:-$ROOT/.gateway/import_staging}"' in text, script


def test_entrypoint_scripts_keep_execution_contract() -> None:
    for script in ENTRYPOINT_SCRIPTS:
        text = script.read_text(encoding="utf-8")
        assert "--all" in text, script
        assert "--unit-only" in text, script
        assert "--integration" in text, script
        assert "--ci" in text, script
        assert "PYTEST_ADDOPTS" in text, script
        assert "no:cacheprovider" in text, script
