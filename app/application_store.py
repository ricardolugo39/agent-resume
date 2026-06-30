from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "resume_agent.sqlite"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _hash_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()[:16]


def _to_json(value: Any) -> str:
    if hasattr(value, "to_dict"):
        value = value.to_dict()

    return json.dumps(value, indent=2, ensure_ascii=False, default=str)


def init_application_store() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                resume_id TEXT NOT NULL UNIQUE,

                company TEXT,
                role TEXT,
                job_url TEXT,

                status TEXT NOT NULL DEFAULT 'Generated',

                candidate_fit_score REAL,
                apply_recommendation TEXT,
                interview_probability TEXT,
                quality_decision TEXT,
                quality_score REAL,

                jd_hash TEXT NOT NULL,
                resume_hash TEXT NOT NULL,

                job_description TEXT NOT NULL,
                candidate_fit_json TEXT,
                resume_strategy_json TEXT,
                resume_outline_json TEXT,
                quality_gate_json TEXT,

                notes TEXT,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )


def generate_resume_id() -> str:
    today = datetime.now().strftime("%Y%m%d")

    init_application_store()

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT COUNT(*)
            FROM applications
            WHERE resume_id LIKE ?
            """,
            (f"RES-{today}-%",),
        ).fetchone()

    next_number = int(row[0]) + 1

    return f"RES-{today}-{next_number:03d}"


def save_application_record(
    job_description: str,
    candidate_fit: dict,
    resume_strategy: dict,
    resume_outline: dict,
    quality_evaluation: Any,
    company: str | None = None,
    role: str | None = None,
    job_url: str | None = None,
    status: str = "Generated",
    notes: str | None = None,
) -> str:
    init_application_store()

    resume_id = generate_resume_id()

    resume_outline_json = _to_json(resume_outline)
    quality_json = _to_json(quality_evaluation)

    jd_hash = _hash_text(job_description)
    resume_hash = _hash_text(resume_outline_json)

    created_at = _now_iso()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO applications (
                resume_id,
                company,
                role,
                job_url,
                status,
                candidate_fit_score,
                apply_recommendation,
                interview_probability,
                quality_decision,
                quality_score,
                jd_hash,
                resume_hash,
                job_description,
                candidate_fit_json,
                resume_strategy_json,
                resume_outline_json,
                quality_gate_json,
                notes,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                resume_id,
                company,
                role,
                job_url,
                status,
                candidate_fit.get("candidate_fit_score"),
                candidate_fit.get("apply_recommendation"),
                candidate_fit.get("interview_probability"),
                getattr(quality_evaluation, "decision", None),
                getattr(quality_evaluation, "interview_readiness_score", None),
                jd_hash,
                resume_hash,
                job_description,
                _to_json(candidate_fit),
                _to_json(resume_strategy),
                resume_outline_json,
                quality_json,
                notes,
                created_at,
                created_at,
            ),
        )

    return resume_id