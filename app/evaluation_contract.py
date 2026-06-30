from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Literal


Decision = Literal["PASS", "PASS_WITH_WARNINGS", "FAIL"]
Severity = Literal["critical", "major", "minor"]
Confidence = Literal["high", "medium", "low"]
ResumeArea = Literal[
    "summary",
    "skills",
    "experience",
    "company_section",
    "bullet",
    "ats",
    "overall",
]


@dataclass
class EvaluationFinding:
    criterion: str
    rule_id: str
    severity: Severity
    confidence: Confidence
    finding: str
    evidence: str
    required_action: str
    applies_to: list[ResumeArea] = field(default_factory=list)


@dataclass
class EvaluationStrength:
    criterion: str
    reason: str
    applies_to: list[ResumeArea] = field(default_factory=list)


@dataclass
class EvaluationMetadata:
    rqs_version: str = "0.1"
    generator_version: str | None = None
    evaluation_model: str | None = None
    jd_hash: str | None = None
    resume_hash: str | None = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

@dataclass
class RewritePlan:
    rewrite_summary: bool = False
    rewrite_experience_order: bool = False
    rewrite_skills: bool = False
    rewrite_company_sections: list[str] = field(default_factory=list)
    rewrite_bullets: list[str] = field(default_factory=list)
    focus: list[str] = field(default_factory=list)

@dataclass
class ResumeEvaluation:
    decision: Decision
    interview_readiness_score: int
    summary: str
    iterations: int = 1
    findings: list[EvaluationFinding] = field(default_factory=list)
    strengths: list[EvaluationStrength] = field(default_factory=list)
    rewrite_prompt: str = ""
    rewrite_plan: RewritePlan = field(default_factory=RewritePlan)
    metadata: EvaluationMetadata = field(default_factory=EvaluationMetadata)
    

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def has_blocking_findings(self) -> bool:
        return any(f.severity == "critical" for f in self.findings)

    @property
    def major_findings_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "major")

    @property
    def minor_findings_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "minor")