from __future__ import annotations


def build_rewrite_plan(evaluation: dict) -> dict:
    """
    Converts Quality Gate findings into a structured rewrite plan
    for the Generator.

    This planner never evaluates the resume.
    It only translates Quality Gate feedback into actionable
    generation instructions.
    """

    plan = {
        "rewrite_summary": False,
        "rewrite_experience_order": False,
        "rewrite_skills": False,
        "rewrite_company_sections": [],
        "rewrite_bullets": [],
        "focus": [],
    }

    findings = evaluation.get("findings", [])

    for finding in findings:

        applies = finding.get("applies_to", [])

        if "summary" in applies:
            plan["rewrite_summary"] = True

        if "skills" in applies:
            plan["rewrite_skills"] = True

        if "experience" in applies:
            plan["rewrite_experience_order"] = True

        if "company_section" in applies:
            plan["rewrite_company_sections"].append(
                finding["required_action"]
            )

        if "bullet" in applies:
            plan["rewrite_bullets"].append(
                finding["required_action"]
            )

        plan["focus"].append(
            finding["required_action"]
        )

    return plan