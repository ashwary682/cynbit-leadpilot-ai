"""SQLite persistence for the prototype (PostgreSQL would replace this in production)."""
import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from .models import LeadAnalysis
from .scoring import LeadScore

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leads.db"


def _conn(db_path=DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            inquiry TEXT, analysis_json TEXT, score INTEGER, tier TEXT, email_draft TEXT)"""
    )
    return conn


def save_lead(inquiry: str, a: LeadAnalysis, s: LeadScore, email: str, db_path=DB_PATH) -> int:
    with _conn(db_path) as c:
        cur = c.execute(
            "INSERT INTO leads (inquiry, analysis_json, score, tier, email_draft) VALUES (?,?,?,?,?)",
            (inquiry, a.model_dump_json(), s.total, s.tier, email),
        )
        return cur.lastrowid


def list_leads(limit: int = 50, db_path=DB_PATH):
    with _conn(db_path) as c:
        rows = c.execute(
            "SELECT id, created_at, score, tier, analysis_json FROM leads ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    out = []
    for id_, ts, score, tier, aj in rows:
        d = json.loads(aj)
        out.append({"id": id_, "created_at": ts, "score": score, "tier": tier,
                    "client": d.get("client_name"), "company": d.get("company"),
                    "category": d.get("service_category"), "urgency": d.get("urgency")})
    return out
