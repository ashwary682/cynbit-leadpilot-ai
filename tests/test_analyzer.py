import pytest

from src.analyzer import _parse_budget, _parse_timeline, analyze_inquiry, rule_based_extract
from src.samples import SAMPLES
from src.scoring import score_lead
from src.storage import list_leads, save_lead


def test_budget_parsing():
    assert _parse_budget("budget is INR 3 lakh")[1] == 300000
    assert _parse_budget("Budget $4,000")[1] == 4000 * 85
    assert _parse_budget("we have 50k rupees")[1] == 50000
    assert _parse_budget("no money info here 2 days")[1] is None


def test_timeline_parsing():
    assert _parse_timeline("in 8 weeks")[1] == 8
    assert _parse_timeline("about 3 months")[1] == pytest.approx(13.0, abs=0.1)
    assert _parse_timeline("nothing")[1] is None


@pytest.mark.parametrize("sample", SAMPLES, ids=[s["name"] for s in SAMPLES])
def test_rule_based_category_on_synthetic_samples(sample):
    assert rule_based_extract(sample["text"]).service_category == sample["expected_category"]


def test_sample_tiers_are_ordered_sensibly():
    scores = {s["name"]: score_lead(rule_based_extract(s["text"])).total for s in SAMPLES}
    assert scores[SAMPLES[0]["name"]] > scores[SAMPLES[2]["name"]]
    assert score_lead(rule_based_extract(SAMPLES[2]["text"])).tier == "Cold"
    assert score_lead(rule_based_extract(SAMPLES[0]["text"])).tier == "Hot"


def test_email_extracted():
    assert rule_based_extract(SAMPLES[0]["text"]).contact_email == "rohan@brightcart.example"


def test_empty_input_raises():
    with pytest.raises(ValueError):
        analyze_inquiry("   ")


def test_falls_back_without_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    r = analyze_inquiry(SAMPLES[0]["text"], use_llm=True)
    assert r.mode == "rule-based"


def test_storage_roundtrip(tmp_path):
    a = rule_based_extract(SAMPLES[0]["text"])
    s = score_lead(a)
    db = tmp_path / "t.db"
    save_lead("txt", a, s, "email", db_path=db)
    rows = list_leads(db_path=db)
    assert len(rows) == 1 and rows[0]["score"] == s.total
