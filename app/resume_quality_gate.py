from __future__ import annotations

import json
from hashlib import sha256
from typing import Any
from app.rewrite_planner import build_rewrite_plan
from app.resume_quality_agent import run_resume_quality_agent
from app.evaluation_contract import (
    EvaluationFinding,
    EvaluationMetadata,
    EvaluationStrength,
    ResumeEvaluation,
    RewritePlan,
)


def _stable_hash(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()[:16]


def serialize_resume_outline(outline: dict) -> str:
    resume_payload = {
        "summary": outline.get("summary"),
        "bullets_by_company": outline.get("bullets_by_company"),
        "selected_achievements": [
            {
                "id": ach.get("id"),
                "company": ach.get("company"),
                "title": ach.get("title"),
                "description": ach.get("description"),
                "business_problem": ach.get("business_problem"),
                "solution": ach.get("solution"),
                "business_impact": ach.get("business_impact"),
                "metrics": ach.get("metrics"),
                "evidence_maturity": ach.get("evidence_maturity"),
                "evidence_type": ach.get("evidence_type"),
                "secondary_evidence_types": ach.get("secondary_evidence_types", []),
            }
            for ach in outline.get("selected_achievements", [])
        ],
    }

    return json.dumps(resume_payload, indent=2, ensure_ascii=False)


def parse_resume_evaluation(
    data: dict[str, Any],
    job_text: str,
    outline: dict,
    iteration: int,
    evaluation_model: str | None = None,
) -> ResumeEvaluation:
    findings = [
        EvaluationFinding(
            criterion=item.get("criterion", "Unknown"),
            rule_id=item.get("rule_id", "RQS-UNKNOWN"),
            severity=item.get("severity", "minor"),
            confidence=item.get("confidence", "medium"),
            finding=item.get("finding", ""),
            evidence=item.get("evidence", ""),
            required_action=item.get("required_action", ""),
            applies_to=item.get("applies_to", []),
        )
        for item in data.get("findings", [])
    ]

    strengths = [
        EvaluationStrength(
            criterion=item.get("criterion", "Unknown"),
            reason=item.get("reason", ""),
            applies_to=item.get("applies_to", []),
        )
        for item in data.get("strengths", [])
    ]

    resume_payload = serialize_resume_outline(outline)

    rewrite_plan = build_rewrite_plan(data)
    typed_rewrite_plan = RewritePlan(**rewrite_plan)

    return ResumeEvaluation(
        decision=data.get("decision", "FAIL"),
        interview_readiness_score=int(data.get("interview_readiness_score", 0)),
        summary=data.get("summary", ""),
        iterations=iteration,
        findings=findings,
        strengths=strengths,
        rewrite_prompt=data.get("rewrite_prompt", ""),
        rewrite_plan=typed_rewrite_plan,
        metadata=EvaluationMetadata(
            rqs_version="0.1",
            evaluation_model=evaluation_model,
            jd_hash=_stable_hash(job_text),
            resume_hash=_stable_hash(resume_payload),
        ),
    )


def evaluate_resume_quality(
    job_text: str,
    outline: dict,
    candidate_fit: dict | None = None,
    resume_strategy: dict | None = None,
    iteration: int = 1,
    evaluation_model: str | None = None,
) -> ResumeEvaluation:
    resume_payload = serialize_resume_outline(outline)

    if candidate_fit is None:
        candidate_fit = outline.get("candidate_fit")

    data = run_resume_quality_agent(
        job_text=job_text,
        candidate_fit=candidate_fit,
        resume_payload=resume_payload,
        resume_strategy=resume_strategy,
        iteration=iteration,
    )

    return parse_resume_evaluation(
        data=data,
        job_text=job_text,
        outline=outline,
        iteration=iteration,
        evaluation_model=evaluation_model,
    )