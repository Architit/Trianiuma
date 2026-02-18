# ROADMAP — Trianiuma

## Governance Baseline (Derived from RADRILONIUMA-PROJECT SoT)

Status: ACTIVE (baseline establishment)
- 2026-02-13 — governance: roadmap observability marker added for drift alignment

### Scope
- contracts-first
- observability-first
- derivation-only
- no runtime logic
- no execution-path impact

### Required governance artifacts
- INTERACTION_PROTOCOL.md
- ROADMAP.md
- DEV_LOGS.md
- WORKFLOW_SNAPSHOT_CONTRACT.md
- WORKFLOW_SNAPSHOT_STATE.md
- SYSTEM_STATE_CONTRACT.md
- SYSTEM_STATE.md
- [x] 2026-02-13 — governance: restart semantics normalized (ACTIVE -> Phase 1 EXPORT, NEW -> Phase 2 IMPORT)
- [x] 2026-02-13 — governance: protocol sync header aligned to RADRILONIUMA-PROJECT/v1.0.0@7eadfe9 [protocol-sync-header-v1]
- [x] 2026-02-16 — governance: S1 cross-repo sync checkpoint aligned to RADRILONIUMA-PROJECT SoT (`t7 ACTIVE long-running`, `t68 ACTIVE hygiene wave`, `phase8.0 readiness in queue`)

## 2026-02-17 Expansion Wave

- Added deterministic pytest baseline (`pytest.ini`).
- Expanded tests from 1 smoke marker to 6 checks.
- Added governance checks for required artifacts and protocol sync markers.
- Added archlog topology checks for `Δ.ref/Δ.raw/Δ.snap/Δ.tasks/Δ.decisions/Δ.risks` branches.
- Added gateway script contract checks for verify/export/import command surface.
- Added unified launcher: `scripts/test_entrypoint.sh`.
- Added archlog content contract checks for reference/raw formats (`tests/test_archlog_content_contract.py`).
- Expansion verification refreshed (`8 passed`).
- Added gateway contract + test entrypoint mode checks (`tests/test_gateway_contract_and_entrypoint.py`).
- Expansion verification refreshed (`10 passed`).
- Added negative-path gateway CLI checks for unknown command and missing import archive (`tests/test_gateway_io_negative_paths.py`).
- Expansion verification refreshed (`12 passed`).
