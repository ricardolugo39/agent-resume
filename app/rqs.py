from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Severity = Literal["critical", "major", "minor"]


@dataclass(frozen=True)
class RQSRule:
    id: str
    criterion: str
    title: str
    description: str
    severity: Severity


RQS_RULES = [

    # ------------------------------------------------------------------
    # INTERVIEW OBJECTIVE
    # ------------------------------------------------------------------

    RQSRule(
        id="RQS-001",
        criterion="Interview Objective",
        title="Interview First",
        description=(
            "The resume must maximize the probability of earning an interview. "
            "Every section should contribute toward that objective."
        ),
        severity="critical",
    ),

    RQSRule(
        id="RQS-002",
        criterion="Interview Objective",
        title="Role Relevance",
        description=(
            "The resume must emphasize the experience most relevant to the target "
            "role instead of attempting to document the entire career."
        ),
        severity="critical",
    ),

    # ------------------------------------------------------------------
    # POSITIONING
    # ------------------------------------------------------------------

    RQSRule(
        id="RQS-101",
        criterion="Positioning",
        title="Clear Professional Identity",
        description=(
            "The resume should communicate one coherent professional identity "
            "supported by the evidence."
        ),
        severity="critical",
    ),

    RQSRule(
        id="RQS-102",
        criterion="Positioning",
        title="Differentiation",
        description=(
            "The resume should clearly communicate why Ricardo is more compelling "
            "than similar candidates."
        ),
        severity="major",
    ),

    # ------------------------------------------------------------------
    # EVIDENCE
    # ------------------------------------------------------------------

    RQSRule(
        id="RQS-201",
        criterion="Evidence",
        title="Evidence Based",
        description=(
            "Every important claim must be directly supported by candidate evidence."
        ),
        severity="critical",
    ),

    RQSRule(
        id="RQS-202",
        criterion="Evidence",
        title="No Hallucinations",
        description=(
            "The resume must never invent achievements, metrics, ownership, "
            "technologies, business outcomes, or domain expertise."
        ),
        severity="critical",
    ),

    RQSRule(
        id="RQS-203",
        criterion="Evidence",
        title="Credible Positioning",
        description=(
            "Positioning must reflect proven experience first and adjacent "
            "experience second."
        ),
        severity="critical",
    ),

    # ------------------------------------------------------------------
    # PM SIGNALS
    # ------------------------------------------------------------------

    RQSRule(
        id="RQS-301",
        criterion="PM Competencies",
        title="Product Judgment",
        description=(
            "When applicable, the resume should demonstrate product judgment "
            "through prioritization, tradeoffs, customer understanding, "
            "or product decisions."
        ),
        severity="major",
    ),

    RQSRule(
        id="RQS-302",
        criterion="PM Competencies",
        title="Ownership",
        description=(
            "The resume should communicate ownership rather than participation."
        ),
        severity="major",
    ),

    RQSRule(
        id="RQS-303",
        criterion="PM Competencies",
        title="Business Outcomes",
        description=(
            "Achievements should emphasize business or customer outcomes rather "
            "than task completion."
        ),
        severity="major",
    ),

    # ------------------------------------------------------------------
    # WRITING
    # ------------------------------------------------------------------

    RQSRule(
        id="RQS-401",
        criterion="Writing",
        title="Accomplishment Focus",
        description=(
            "Bullets should emphasize accomplishments instead of responsibilities."
        ),
        severity="major",
    ),

    RQSRule(
        id="RQS-402",
        criterion="Writing",
        title="Readable Structure",
        description=(
            "The resume should be easy to scan with concise, well-organized content."
        ),
        severity="minor",
    ),

    RQSRule(
        id="RQS-403",
        criterion="Writing",
        title="ATS Compatible",
        description=(
            "Formatting should remain compatible with modern ATS systems."
        ),
        severity="minor",
    ),
]


RULES_BY_ID = {
    rule.id: rule
    for rule in RQS_RULES
}


RULES_BY_CRITERION = {}

for rule in RQS_RULES:
    RULES_BY_CRITERION.setdefault(rule.criterion, []).append(rule)


def get_rule(rule_id: str) -> RQSRule:
    return RULES_BY_ID[rule_id]


def get_rules_for_criterion(criterion: str) -> list[RQSRule]:
    return RULES_BY_CRITERION.get(criterion, [])


def get_all_rules() -> list[RQSRule]:
    return RQS_RULES