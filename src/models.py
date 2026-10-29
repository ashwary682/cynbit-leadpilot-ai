"""Pydantic data models: the structured contract between the LLM and the rest of the app."""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

SERVICE_CATEGORIES = [
    "AI/LLM Automation",
    "Chatbot / AI Agent",
    "Document Processing",
    "CRM / Workflow Automation",
    "Web / SaaS Development",
    "Mobile App Development",
    "Data / ML Solution",
    "Other",
]


class LeadAnalysis(BaseModel):
    """Structured information extracted from a free-text customer inquiry."""

    client_name: Optional[str] = None
    company: Optional[str] = None
    contact_email: Optional[str] = None
    service_category: str = "Other"
    project_summary: str = ""
    requirements: List[str] = Field(default_factory=list)
    budget_text: Optional[str] = None
    budget_inr: Optional[float] = None  # approximate, in INR
    timeline_text: Optional[str] = None
    timeline_weeks: Optional[float] = None
    urgency: Literal["low", "medium", "high"] = "medium"
    missing_info: List[str] = Field(default_factory=list)

    @field_validator("service_category", mode="before")
    @classmethod
    def _valid_category(cls, v):
        return v if v in SERVICE_CATEGORIES else "Other"

    @field_validator("requirements", "missing_info", mode="before")
    @classmethod
    def _none_to_list(cls, v):
        return [] if v is None else v

    @field_validator("urgency", mode="before")
    @classmethod
    def _norm_urgency(cls, v):
        v = str(v).lower().strip() if v is not None else "medium"
        return v if v in ("low", "medium", "high") else "medium"

    @field_validator("project_summary", mode="before")
    @classmethod
    def _none_to_str(cls, v):
        return "" if v is None else v


def compute_missing_info(a: LeadAnalysis) -> List[str]:
    """Deterministic missing-info check (we do not trust the LLM for this)."""
    missing = []
    if not a.budget_inr and not a.budget_text:
        missing.append("Budget or budget range")
    if not a.timeline_weeks and not a.timeline_text:
        missing.append("Expected timeline / launch date")
    if len(a.requirements) < 2:
        missing.append("Detailed requirements (features, users, integrations)")
    if not a.contact_email:
        missing.append("Contact email")
    if not a.company:
        missing.append("Company / organisation name")
    if a.service_category == "Other":
        missing.append("Clear service type (AI, web app, automation, etc.)")
    return missing
