from __future__ import annotations

import json

from app.candidate_fit_protocol import CANDIDATE_FIT_PROTOCOL


def build_candidate_fit_prompt(
    job_text: str,
    ricardo_profile: str,
    experiences: list[dict],
    achievements: list[dict],
) -> str:
    return f"""
{CANDIDATE_FIT_PROTOCOL}

Evaluate Ricardo's candidate fit for the following role.

Return ONLY valid JSON.

Required JSON schema:
{{
  "apply_recommendation": "APPLY | APPLY_IF_INTERESTED | STRETCH | DO_NOT_APPLY",
  "candidate_fit_score": 0.0,
  "interview_probability": "HIGH | MEDIUM_HIGH | MEDIUM | LOW",
  "confidence": "high | medium | low",
  "summary": "short candidate fit summary",
  "recommended_positioning": "strongest truthful positioning",
  "strategy_guidance": "guidance for the downstream resume strategy agent",
  "proven_matches": [
    {{
      "category": "Enterprise Analytics",
      "evidence": "specific evidence from Ricardo's background",
      "confidence": "high | medium | low"
    }}
  ],
  "credible_adjacencies": [
    {{
      "category": "Customer Data Products",
      "rationale": "why this is adjacent but not direct",
      "transferable_evidence": "specific transferable evidence"
    }}
  ],
  "hard_gaps": [
    {{
      "category": "CDP / MDM",
      "explanation": "why this is a real gap",
      "severity": "critical | major | minor"
    }}
  ],
  "biggest_strengths": [
    {{
      "title": "Enterprise analytics product ownership",
      "explanation": "why this matters for the role"
    }}
  ],
  "biggest_risks": [
    {{
      "title": "No direct CDP ownership",
      "explanation": "why this may reduce interview probability"
    }}
  ],
  "recruiter_concerns": [
    {{
      "concern": "possible recruiter concern",
      "why_it_matters": "why it could affect screening",
      "mitigation": "how positioning can reduce the concern"
    }}
  ],
  "hiring_manager_concerns": [
    {{
      "concern": "possible hiring manager concern",
      "why_it_matters": "why it could affect interview decision",
      "mitigation": "how strategy can reduce the concern"
    }}
  ]
}}

Scoring guidance:
- 9.0-10.0: Exceptional fit with strong direct evidence.
- 8.0-8.9: Strong fit with mostly direct evidence.
- 7.0-7.9: Good but imperfect fit; likely worth applying if interested.
- 6.0-6.9: Stretch; apply only if the role is strategically attractive.
- Below 6.0: Weak fit.

Recommendation guidance:
- APPLY: strong or very strong candidate fit.
- APPLY_IF_INTERESTED: credible fit but not a must-apply.
- STRETCH: meaningful gaps; possible but lower probability.
- DO_NOT_APPLY: weak fit or severe unsupported requirements.

Important:
- Do not evaluate the generated resume.
- Do not write or rewrite resume bullets.
- Do not inflate fit because of keyword overlap.
- Do not hide hard gaps.
- Distinguish direct evidence from adjacent evidence.
- Recommended positioning must be truthful and grounded in the evidence.

Ricardo Profile:
{ricardo_profile}

Experiences:
{json.dumps(experiences, indent=2, ensure_ascii=False)}

Achievement Evidence:
{json.dumps(achievements, indent=2, ensure_ascii=False)}

Job Description:
{job_text}
"""