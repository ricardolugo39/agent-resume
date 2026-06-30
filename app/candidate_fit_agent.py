from __future__ import annotations

from typing import Any

from app.base_agent import BaseAgent
from app.candidate import Candidate
from app.candidate_fit_prompt_builder import build_candidate_fit_prompt


class CandidateFitAgent(BaseAgent):
    """
    Evaluates Ricardo's competitiveness for a specific role.

    This agent evaluates the candidate, NOT the resume.
    """

    def build_prompt(
        self,
        candidate: Candidate,
        job_text: str,
    ) -> str:

        return build_candidate_fit_prompt(
            job_text=job_text,
            ricardo_profile=candidate.profile,
            experiences=candidate.experiences,
            achievements=candidate.achievements,
        )

    def parse_response(
        self,
        raw_response: str,
    ) -> dict[str, Any]:

        return self.extract_json_object(raw_response)


def evaluate_candidate_fit(
    job_text: str,
    candidate_name: str = "ricardo",
) -> dict[str, Any]:

    candidate = Candidate.load(candidate_name)

    agent = CandidateFitAgent()

    return agent.run(
        candidate=candidate,
        job_text=job_text,
    )