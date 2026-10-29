from src.models import LeadAnalysis, compute_missing_info
from src.scoring import score_lead


def full_lead(**kw):
    base = dict(client_name="A", company="B", contact_email="a@b.com", service_category="Chatbot / AI Agent",
                requirements=["x", "y", "z"], budget_inr=300000, timeline_weeks=8, urgency="high")
    base.update(kw)
    return LeadAnalysis(**base)


def test_complete_lead_scores_hot_and_max():
    s = score_lead(full_lead())
    assert s.total == 100 and s.tier == "Hot"


def test_empty_lead_scores_cold():
    s = score_lead(LeadAnalysis())
    assert s.tier == "Cold" and s.total < 30


def test_score_items_sum_to_total():
    s = score_lead(full_lead(budget_inr=None, budget_text="flexible"))
    assert sum(i.points for i in s.items) == s.total


def test_unrealistic_timeline_penalised():
    fast = score_lead(full_lead(timeline_weeks=1)).total
    ok = score_lead(full_lead(timeline_weeks=8)).total
    assert fast < ok


def test_missing_info_detects_gaps():
    m = compute_missing_info(LeadAnalysis())
    assert any("Budget" in x for x in m) and any("timeline" in x.lower() for x in m)


def test_invalid_category_and_urgency_are_normalised():
    a = LeadAnalysis(service_category="Banana", urgency="EXTREME", requirements=None)
    assert a.service_category == "Other" and a.urgency == "medium" and a.requirements == []
