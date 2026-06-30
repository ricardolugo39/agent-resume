from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ApplyRecommendation = Literal[
    "APPLY",
    "APPLY_IF_INTERESTED",
    "STRETCH",
    "DO_NOT_APPLY",
]

InterviewProbability = Literal[
    "HIGH",
    "MEDIUM_HIGH",
    "MEDIUM",
    "LOW",
]


@dataclass
class ProvenMatch:
    category: str
    evidence: str
    confidence: str


@dataclass
class CredibleAdjacency:
    category: str
    rationale: str
    transferable_evidence: str


@dataclass
class HardGap:
    category: str
    explanation: str
    severity: Literal["critical", "major", "minor"]


@dataclass
class RecruiterConcern:
    concern: str
    why_it_matters: str
    mitigation: str


@dataclass
class HiringManagerConcern:
    concern: str
    why_it_matters: str
    mitigation: str


@dataclass
class CandidateStrength:
    title: str
    explanation: str


@dataclass
class CandidateRisk:
    title: str
    explanation: str


@dataclass
class CandidateFitEvaluation:

    #
    # Overall recommendation
    #

    apply_recommendation: ApplyRecommendation

    candidate_fit_score: float

    interview_probability: InterviewProbability

    confidence: Literal[
        "high",
        "medium",
        "low",
    ]

    #
    # Executive summary
    #

    summary: str

    recommended_positioning: str

    strategy_guidance: str

    #
    # Evaluation
    #

    proven_matches: list[ProvenMatch] = field(default_factory=list)

    credible_adjacencies: list[CredibleAdjacency] = field(default_factory=list)

    hard_gaps: list[HardGap] = field(default_factory=list)

    biggest_strengths: list[CandidateStrength] = field(default_factory=list)

    biggest_risks: list[CandidateRisk] = field(default_factory=list)

    recruiter_concerns: list[RecruiterConcern] = field(default_factory=list)

    hiring_manager_concerns: list[HiringManagerConcern] = field(default_factory=list)