"""Explainable, rule-based lead scoring.

IMPORTANT: this score is a *prioritisation heuristic* based on how complete and
actionable an inquiry is. It is NOT a prediction of sales conversion. It has not
been validated against real historical Cynbit data.
Thresholds below are assumptions and should be tuned with real data.
"""
from dataclasses import dataclass
from typing import List

from .models import LeadAnalysis

# --- Tunable assumptions -------------------------------------------------
BUDGET_LOW_INR = 50_000
BUDGET_HIGH_INR = 200_000
HOT_THRESHOLD = 75
WARM_THRESHOLD = 50
# -------------------------------------------------------------------------


@dataclass
class ScoreItem:
    factor: str
    points: int
    max_points: int
    reason: str


@dataclass
class LeadScore:
    total: int
    tier: str
    items: List[ScoreItem]


def _service_fit(a: LeadAnalysis) -> ScoreItem:
    if a.service_category != "Other":
        return ScoreItem("Service fit", 25, 25, f"Matches a service area: {a.service_category}")
    return ScoreItem("Service fit", 5, 25, "Could not match to a clear service area")


def _requirements(a: LeadAnalysis) -> ScoreItem:
    n = len(a.requirements)
    pts = 0 if n == 0 else 8 if n == 1 else 14 if n == 2 else 20
    return ScoreItem("Requirement clarity", pts, 20, f"{n} concrete requirement(s) identified")


def _budget(a: LeadAnalysis) -> ScoreItem:
    if a.budget_inr:
        if a.budget_inr >= BUDGET_HIGH_INR:
            return ScoreItem("Budget", 20, 20, f"Budget ~INR {a.budget_inr:,.0f} (substantial)")
        if a.budget_inr >= BUDGET_LOW_INR:
            return ScoreItem("Budget", 14, 20, f"Budget ~INR {a.budget_inr:,.0f} (moderate)")
        return ScoreItem("Budget", 8, 20, f"Budget ~INR {a.budget_inr:,.0f} (low for custom work)")
    if a.budget_text:
        return ScoreItem("Budget", 6, 20, "Budget mentioned but amount unclear")
    return ScoreItem("Budget", 0, 20, "No budget mentioned")


def _timeline(a: LeadAnalysis) -> ScoreItem:
    w = a.timeline_weeks
    if w:
        if w < 2:
            return ScoreItem("Timeline", 6, 15, f"~{w:.1f} weeks: likely unrealistic")
        if w <= 52:
            return ScoreItem("Timeline", 15, 15, f"~{w:.1f} weeks: clear and realistic")
        return ScoreItem("Timeline", 10, 15, f"~{w:.0f} weeks: very long horizon")
    if a.timeline_text:
        return ScoreItem("Timeline", 8, 15, "Timeline mentioned but vague")
    return ScoreItem("Timeline", 0, 15, "No timeline mentioned")


def _contact(a: LeadAnalysis) -> ScoreItem:
    pts = (6 if a.contact_email else 0) + (2 if a.client_name else 0) + (2 if a.company else 0)
    return ScoreItem("Contact completeness", pts, 10, "Email +6, name +2, company +2")


def _urgency(a: LeadAnalysis) -> ScoreItem:
    pts = {"high": 10, "medium": 6, "low": 3}[a.urgency]
    return ScoreItem("Urgency", pts, 10, f"Urgency detected: {a.urgency}")


def score_lead(a: LeadAnalysis) -> LeadScore:
    items = [_service_fit(a), _requirements(a), _budget(a), _timeline(a), _contact(a), _urgency(a)]
    total = sum(i.points for i in items)
    tier = "Hot" if total >= HOT_THRESHOLD else "Warm" if total >= WARM_THRESHOLD else "Cold"
    return LeadScore(total=total, tier=tier, items=items)
