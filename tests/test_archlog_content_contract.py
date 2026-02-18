from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_ref_contract_contains_required_sections():
    ref_files = list((REPO_ROOT / "archlogcore" / "Δ.ref").rglob("*.md"))
    assert ref_files, "missing Δ.ref markdown files"
    text = ref_files[0].read_text(encoding="utf-8")
    assert "meta:" in text
    assert "paths:" in text
    assert "commands:" in text
    assert "templates:" in text


def test_raw_contract_contains_expected_fields():
    raw_files = list((REPO_ROOT / "archlogcore" / "Δ.raw").rglob("*.yaml"))
    assert raw_files, "missing Δ.raw yaml files"
    text = raw_files[0].read_text(encoding="utf-8")
    assert "meta:" in text
    assert "state:" in text
    assert "focus:" in text
    assert "risks:" in text
