import json

from app.llm_client import call_openai


def clean_bullets(raw_text: str) -> list[str]:
    lines = []

    for line in raw_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("-"):
            lines.append(line)
        else:
            lines.append(f"- {line}")

    return lines


def generate_company_section(
    company: str,
    achievements: list[dict],
    parsed_job: dict,
    resume_strategy: dict | None = None,
    max_bullets: int = 3
) -> list[str]:

    if resume_strategy is None:
        resume_strategy = {}

    winning_story = resume_strategy.get("winning_story", "")
    primary_angle = resume_strategy.get("primary_angle", "")
    secondary_angle = resume_strategy.get("secondary_angle", "")
    avoid_angle = resume_strategy.get("avoid_angle", "")

    strategy_payload = {
        "winning_story": winning_story,
        "primary_angle": primary_angle,
        "secondary_angle": secondary_angle,
        "avoid_angle": avoid_angle,
        "target_positioning": resume_strategy.get("target_positioning"),
        "resume_narrative": resume_strategy.get("resume_narrative"),
        "selection_priorities": resume_strategy.get("selection_priorities"),
        "keywords_to_include": resume_strategy.get("keywords_to_include"),
        "keywords_to_avoid_overclaiming": resume_strategy.get("keywords_to_avoid_overclaiming"),
        "bullet_strategy": resume_strategy.get("bullet_strategy"),
        "tone": resume_strategy.get("tone"),
    }

    prompt = f"""
You are writing one cohesive resume experience section for Ricardo Lugo.

Company:
{company}

Target positioning:
{resume_strategy.get("target_positioning", parsed_job.get("role_type", "Product Manager"))}

Winning story:
{winning_story}

Primary angle:
{primary_angle}

Secondary angle:
{secondary_angle}

Avoid angle:
{avoid_angle}

Resume strategy:
{json.dumps(strategy_payload, indent=2)}

Selected achievements for this company:
{json.dumps(achievements, indent=2)}

Task:
Write exactly {max_bullets} resume bullets for this company.

The bullets should read like a top-tier resume experience section.

Think about the company section as a whole:
- Avoid repetition.
- Vary emphasis across bullets.
- Different bullets may highlight customer discovery, product strategy, roadmap ownership, adoption, platform decisions, technical execution, experimentation, UX, stakeholder influence, or business outcomes.
- The section should feel cohesive and human-written.

Important:
- The achievements are the source of truth.
- The resume strategy determines emphasis, not facts.
- Do not invent facts in order to better match the target role.
- Do not introduce terminology from the JD unless supported by the achievements.
- Every bullet must be traceable to one or more achievements provided for this company.

Truth rules:
- Use ONLY the selected achievements provided for this company.
- Do not borrow facts from the job description, resume strategy, or other companies.
- Do not mention products, platforms, tools, metrics, or company-specific terms from other companies.
- If a term appears in the resume strategy but not in this company's achievements, do not use it.
- Do not invent domain expertise, customer types, industries, tools, metrics, technical environments, operational contexts, or scope.
- Preserve verified metrics exactly.
- Do not introduce AI, ML, LLM, agentic, copilot, recommendation system, personalization, embedded systems, firmware, hardware, SaaS, enterprise, customer type, or industry claims unless explicitly supported by this company's selected achievements.

Writing rules:
- Write like a top-tier executive resume writer, not a job description.
- The goal is a persuasive, human, recruiter-ready company section.
- Use concrete product language over abstract PM jargon.
- Vary verbs, sentence rhythm, and structure across bullets.
- Avoid starting multiple bullets with the same verb.
- Avoid overusing: Led, Directed, Owned, Managed, Spearheaded, Orchestrated.
- Do not force every bullet into the same structure.
- Avoid robotic phrases like:
  "enhancing platform scalability",
  "driving operational visibility",
  "aligning stakeholder priorities",
  "supporting strategic growth initiatives",
  "user-centric",
  "seamless",
  "robust".
- Avoid overusing dashboards, analytics, forecasting, automation, operational visibility, KPI language, or reporting unless the achievements clearly require it.
- If a domain is only adjacent, keep the framing transferable and credible.
- Keep each bullet concise but complete.
- Output only bullets, one per line, each starting with "-".
"""

    raw = call_openai(prompt)
    bullets = clean_bullets(raw)

    return bullets[:max_bullets]