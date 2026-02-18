from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_archlogcore_branches_present():
    base = REPO_ROOT / "archlogcore"
    required = [
        "Δ.ref",
        "Δ.raw",
        "Δ.snap",
        "Δ.tasks",
        "Δ.decisions",
        "Δ.risks",
    ]
    missing = [name for name in required if not (base / name).exists()]
    assert not missing, f"missing archlog branches: {missing}"


def test_archlog_reference_and_raw_examples_present():
    ref_files = list((REPO_ROOT / "archlogcore" / "Δ.ref").rglob("*.md"))
    raw_files = list((REPO_ROOT / "archlogcore" / "Δ.raw").rglob("*.yaml"))
    assert ref_files, "no reference markdown files found in Δ.ref"
    assert raw_files, "no raw yaml files found in Δ.raw"


def test_gateway_script_contains_verify_export_import_contract():
    script = (REPO_ROOT / "scripts" / "gateway_io.sh").read_text(encoding="utf-8")
    assert "verify_github" in script
    assert "verify_onedrive" in script
    assert "verify_gworkspace" in script
    assert "do_export" in script
    assert "do_import" in script
    assert "Usage: $0 [verify|export|import <archive>]" in script
