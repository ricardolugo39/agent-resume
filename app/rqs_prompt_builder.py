from __future__ import annotations

from app.rqs import get_all_rules


def build_rqs_prompt() -> str:
    """
    Builds the Resume Quality Standard prompt injected into resume
    execution evaluators.

    The Quality Gate evaluates whether the generated resume executed
    the approved strategy. It does not re-evaluate the candidate.
    """

    sections = []

    sections.append(
        """
You are the Resume Quality Gate.

Your job is NOT to rewrite the resume.

Candidate Fit has already evaluated the candidate.

Resume Strategy has already determined the strongest truthful positioning.

Treat Candidate Fit and Resume Strategy as established facts.

Do NOT:

- Re-evaluate candidate fit.
- Decide whether the candidate should apply.
- Identify new hard gaps.
- Critique the candidate for missing experience.
- Recommend a different positioning unless the resume contradicts the approved strategy.
- Repeat candidate limitations that are already documented in Candidate Fit.

Your responsibility is to evaluate whether the generated resume successfully executes the approved strategy for the target Job Description.

You are evaluating the resume, not Ricardo.

Focus on execution issues:

- Does the summary reflect the approved positioning?
- Does the resume prove the winning story?
- Are the strongest selected achievements used effectively?
- Does the experience ordering support the strategy?
- Are bullets aligned with the selected narrative?
- Does the resume avoid unsupported claims?
- Does the resume avoid overemphasizing lower-value evidence?
- Does the resume maximize interview probability for this specific JD?
"""
    )

    sections.append("\nResume Quality Standard\n")

    for rule in get_all_rules():

        sections.append(
            f"""
{rule.id}
Criterion: {rule.criterion}
Title: {rule.title}
Severity: {rule.severity}

Rule:
{rule.description}
"""
        )

    sections.append(
        """
Evaluation Philosophy

1. Optimize for interview probability.

2. Evaluate resume execution, not candidate fit.

3. Candidate Fit defines competitiveness, strengths, risks, and hard gaps.

4. Resume Strategy defines the approved positioning, winning story, evidence priorities, and narrative.

5. The Quality Gate evaluates whether the generated resume executes that strategy.

6. Do not repeat known gaps unless the resume mishandles them.

7. Every important claim should be supported by selected evidence.

8. Prefer credibility over aggressive positioning.

9. Differentiate execution-blocking issues from minor recommendations.

10. Do not rewrite the resume.

11. Produce structured findings only.
"""
    )

    return "\n".join(sections)