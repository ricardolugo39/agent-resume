import json
from pathlib import Path

from app.llm_client import call_openai
from app.resume_writing_guide import WRITING_GUIDE


BASE_DIR = Path(__file__).resolve().parents[1]
PROMPT_PATH = BASE_DIR / "app" / "prompts" / "bullet_rewrite_prompt.txt"


def load_prompt_template() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def rewrite_bullet(
    achievement: dict,
    parsed_job: dict,
    resume_strategy: dict | None = None,
    rewrite_plan: dict | None = None,
) -> str:

    template = load_prompt_template()

    template = f"""
    Resume Writing Guide

    {WRITING_GUIDE}

    {template}
    """

    rewrite_focus = ""

    if rewrite_plan:
        rewrite_focus = "\n".join(
            rewrite_plan.get("focus", [])
        )

   

    if resume_strategy is None:
        resume_strategy = {}

    prompt = template.format(
        target_role=resume_strategy.get(
            "target_positioning",
            parsed_job.get("role_type", "Product Manager")
        ),
        job_keywords=", ".join(parsed_job.get("keywords", [])),
        job_description=parsed_job.get("raw_text", ""),
        resume_strategy=json.dumps({
            "target_positioning": resume_strategy.get("target_positioning"),
            "resume_narrative": resume_strategy.get("resume_narrative"),
            "role_dimensions": resume_strategy.get("role_dimensions"),
            "selection_priorities": resume_strategy.get("selection_priorities"),
            "primary_strengths": resume_strategy.get("primary_strengths"),
            "credible_adjacencies": resume_strategy.get("credible_adjacencies"),
            "hard_gaps": resume_strategy.get("hard_gaps"),
            "keywords_to_include": resume_strategy.get("keywords_to_include"),
            "keywords_to_avoid_overclaiming": resume_strategy.get("keywords_to_avoid_overclaiming"),
            "bullet_strategy": resume_strategy.get("bullet_strategy"),
            "tone": resume_strategy.get("tone"),
        }, indent=2),
        achievement=json.dumps(achievement, indent=2),
        rewrite_guidance=rewrite_focus
    )

    bullet = call_openai(prompt)

    bullet = bullet.strip()

    if not bullet.startswith("-"):
        bullet = f"- {bullet}"

    return bullet