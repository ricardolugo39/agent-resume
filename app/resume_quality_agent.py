from __future__ import annotations

import json
from typing import Any

from app.base_agent import BaseAgent
from app.rqs_prompt_builder import build_rqs_prompt


class ResumeQualityAgent(BaseAgent):

    def build_prompt(
      self,
      job_text: str,
      candidate_fit: dict | None,
      resume_payload: str,
      resume_strategy: dict | None = None,
      iteration: int = 1,
  ) -> str:

      return f"""
  {build_rqs_prompt()}

  Job Description
  ---------------
  {job_text}

  Candidate Fit Assessment
  ------------------------
  {json.dumps(candidate_fit or {{}}, indent=2, ensure_ascii=False)}

  Approved Resume Strategy
  ------------------------
  {json.dumps(resume_strategy or {{}}, indent=2, ensure_ascii=False)}

  Generated Resume
  ----------------
  {resume_payload}

  Evaluation Instructions
  -----------------------

  The Candidate Fit Assessment and Resume Strategy are the approved baseline.

  Evaluate ONLY whether the generated resume faithfully executes the approved Resume Strategy.

  The Candidate Fit Assessment provides approved positioning boundaries.

  It is NOT content that must appear in the resume.

  Do NOT:

  - Re-evaluate candidate fit.
  - Determine whether Ricardo should apply.
  - Identify new hard gaps unless the resume introduces unsupported claims.
  - Recommend a different positioning unless the resume contradicts the approved strategy.
  - Repeat candidate limitations already identified in Candidate Fit.
  - Recommend adding known capability gaps, missing experience, or stretch qualifications to the resume unless the resume makes unsupported claims about those areas.
  - Recommend adding statements about what the candidate has not done.

  Resume Philosophy
  -----------------

  A resume is a marketing document designed to maximize interview probability.

  It should emphasize proven strengths.

  It should not volunteer known capability gaps.

  The absence of experience is NOT a resume defect.

  A finding should only be created when the resume:

  - makes an unsupported claim;
  - implies unsupported expertise;
  - contradicts the approved positioning;
  - omits evidence required to support the approved positioning;
  - weakens interview probability through poor writing, weak ordering, or poor evidence use.

  Every finding must describe an execution issue.

  Examples of execution issues include:

  - The summary does not reflect the approved positioning.
  - The resume fails to prove the winning story.
  - The strongest evidence was not selected.
  - Experience ordering weakens the narrative.
  - Bullets emphasize secondary themes instead of the primary angle.
  - Unsupported claims reduce credibility.
  - Important supporting evidence is missing.
  - The resume does not maximize interview probability for this specific role.

  When evaluating the summary:

  - Do NOT penalize the summary because it omits known gaps identified during Candidate Fit.
  - Only evaluate whether the summary accurately reflects the approved positioning.
  - Only evaluate whether the summary is supported by selected evidence.
  - Only evaluate whether the summary maximizes interview probability.
  - Only evaluate whether the summary avoids unsupported claims.

  Focus on:

  1. Summary execution.
  2. Positioning execution.
  3. Winning story execution.
  4. Evidence selection.
  5. Experience ordering.
  6. Bullet quality.
  7. Evidence credibility.
  8. ATS alignment.
  9. Overall interview readiness.

  Required JSON schema:
  {{
    "decision": "PASS | PASS_WITH_WARNINGS | FAIL",
    "interview_readiness_score": 0,
    "summary": "short execution evaluation summary",
    "findings": [
      {{
        "criterion": "Strategy Execution",
        "rule_id": "RQS-101",
        "severity": "critical | major | minor",
        "confidence": "high | medium | low",
        "finding": "execution issue only",
        "evidence": "why this is an execution issue",
        "required_action": "what the generator must improve",
        "applies_to": ["summary", "experience", "company_section", "bullet", "skills", "ats", "overall"]
      }}
    ],
    "strengths": [
      {{
        "criterion": "Strategy Execution",
        "reason": "what the resume executed well",
        "applies_to": ["summary", "experience", "company_section", "bullet", "skills", "ats", "overall"]
      }}
    ],
    "rewrite_prompt": "brief structured instruction for the generator if decision is FAIL or PASS_WITH_WARNINGS"
  }}

  Scoring guidance:

  - interview_readiness_score uses a 1–10 scale.
  - 9.0–10.0: Excellent; ready to submit.
  - 8.0–8.9: Strong; minor polish only.
  - 7.0–7.9: Usable but meaningful improvements remain.
  - 6.0–6.9: Weak execution; rewrite recommended.
  - Below 6.0: Poor execution; major rewrite needed.

  Decision guidance:

  - PASS: Resume executes the approved strategy well and is ready to submit.
  - PASS_WITH_WARNINGS: Resume is usable, but improvements could increase interview probability.
  - FAIL: Resume does not execute the approved strategy and should not be submitted yet.

  Return ONLY valid JSON.

  Evaluation Iteration:
  {iteration}
  """

    def parse_response(
        self,
        raw_response: str,
    ) -> dict[str, Any]:
        return self.extract_json_object(raw_response)


def run_resume_quality_agent(
    job_text: str,
    candidate_fit: dict | None,
    resume_payload: str,
    resume_strategy: dict | None = None,
    iteration: int = 1,
) -> dict[str, Any]:

    agent = ResumeQualityAgent()

    result = agent.run(
        job_text=job_text,
        candidate_fit=candidate_fit,
        resume_payload=resume_payload,
        resume_strategy=resume_strategy,
        iteration=iteration,
    )

    print("=" * 80)
    print("QUALITY GATE RAW PARSED RESULT")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 80)

    return result