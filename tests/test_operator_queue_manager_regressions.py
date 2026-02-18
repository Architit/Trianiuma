from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
QUEUE_MANAGER_PATH = REPO_ROOT / "agents" / "operator-agent" / "agent" / "queue_manager.py"


def _load_queue_manager():
    if "jsonschema" not in sys.modules:
        stub = types.ModuleType("jsonschema")
        stub.validate = lambda *args, **kwargs: None
        stub.ValidationError = Exception
        sys.modules["jsonschema"] = stub
    spec = importlib.util.spec_from_file_location("queue_manager", QUEUE_MANAGER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_iter_pending_handles_invalid_created_at_without_type_error():
    queue_manager = _load_queue_manager()
    items = [
        {
            "id": "task-valid",
            "status": "pending",
            "priority": 10,
            "created_at": "2026-02-18T00:00:00Z",
        },
        {
            "id": "task-invalid",
            "status": "pending",
            "priority": 10,
            "created_at": "not-a-date",
        },
    ]

    ordered = queue_manager.iter_pending(items)

    assert [task["id"] for task in ordered] == ["task-valid", "task-invalid"]
