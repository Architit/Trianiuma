from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PRIMARY = REPO_ROOT / "agents" / "operator-agent" / "agent"
MIRROR = REPO_ROOT / "agents" / "test-agent" / "LAM_Test" / "agents" / "operator-agent" / "agent"

SYNC_FILES = [
    "logger.py",
    "queue_manager.py",
]


def test_operator_agent_mirror_stays_in_sync_for_critical_modules() -> None:
    for rel in SYNC_FILES:
        primary = PRIMARY / rel
        mirror = MIRROR / rel
        assert primary.exists(), primary
        assert mirror.exists(), mirror
        assert primary.read_text(encoding="utf-8") == mirror.read_text(encoding="utf-8"), rel
