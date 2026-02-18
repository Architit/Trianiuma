# Changelog

All notable changes to this repository are documented in this file.

## 2026-02-18

### Added
- `GATEWAY_ACCESS_CONTRACT.md` with gateway verify/export/import contract baseline.
- `pytest.ini` marker registry and deterministic pytest defaults.
- `scripts/ecosystem_health_snapshot.sh` for repository/runtime inventory snapshots.
- `scripts/ecosystem_soak.sh` for repeated ecosystem gate runs with JSON failure payload.
- New ecosystem contract suites under `tests/` for gateway, scripts, shell safety, governance artifacts, archlog surface/content, marker registry, and runtime coverage.

### Changed
- Updated `README.md` and `ROADMAP.md` with entrypoint/testing flow.
- Updated `DEV_LOGS.md` with final hardening-release checkpoints.
- Advanced submodule refs for `agents/operator-agent` and `agents/test-agent` to include runtime and entrypoint test hardening.

### Validation
- Root gate: `scripts/test_entrypoint.sh --all` -> `35 passed`.
- Test-agent gate: `agents/test-agent/scripts/test_entrypoint.sh --all` -> `201 passed`.
- Operator-agent suite: `.venv/bin/pytest -q agents/operator-agent/tests` -> `7 passed`.
