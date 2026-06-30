from app.llm_client import call_openai
from app.resume_writing_guide import WRITING_GUIDE


ROLE_POSITIONING = {
    "technical_pm": "Technical Product Manager",
    "data_pm": "Data & Analytics Product Manager",
    "ai_pm": "AI Product Manager",
    "operations_pm": "Operations Product Manager",
    "industrial_pm": "Industrial Product Manager",
    "growth_pm": "Growth Product Manager",
    "general_pm": "Product Manager",
}


def generate_summary(
    parsed_job: dict,
    selected_achievements: list,
    resume_strategy: dict | None = None,
    rewrite_plan: dict | None = None,
) -> str:

    role_type = parsed_job.get("role_type", "technical_pm")
    keywords = ", ".join(parsed_job.get("keywords", []))
    themes = ", ".join(parsed_job.get("themes", []))

    positioning = (
        resume_strategy.get("target_positioning")
        if resume_strategy
        else ROLE_POSITIONING.get(role_type, "Product Manager")
    )

    winning_story = (
        resume_strategy.get("winning_story", "")
        if resume_strategy
        else ""
    )

    primary_angle = (
        resume_strategy.get("primary_angle", "")
        if resume_strategy
        else ""
    )

    secondary_angle = (
        resume_strategy.get("secondary_angle", "")
        if resume_strategy
        else ""
    )

    avoid_angle = (
        resume_strategy.get("avoid_angle", "")
        if resume_strategy
        else ""
    )

    why_hire = (
        resume_strategy.get("why_hire_this_person", "")
        if resume_strategy
        else ""
    )

    recruiter_pitch = (
        resume_strategy.get("recruiter_pitch", "")
        if resume_strategy
        else ""
    )

    summary_direction = (
        resume_strategy.get("summary_direction", "")
        if resume_strategy
        else ""
    )

    rewrite_focus = ""

    if rewrite_plan:
        rewrite_focus = "\n".join(
            rewrite_plan.get("focus", [])
        )

    evidence = []

    for ach in selected_achievements[:8]:
        evidence.append({
            "company": ach.get("company"),
            "title": ach.get("title"),
            "description": ach.get("description"),
            "metrics": ach.get("metrics"),
            "success_metrics": ach.get("success_metrics"),
            "keywords": ach.get("keywords"),
        })

    strategy_text = ""

    if resume_strategy:
        strategy_text = f"""
    Resume strategy:
    - Winning story: {resume_strategy.get("winning_story")}
    - Primary angle: {resume_strategy.get("primary_angle")}
    - Secondary angle: {resume_strategy.get("secondary_angle")}
    - Avoid angle: {resume_strategy.get("avoid_angle")}
    - Why hire this person: {resume_strategy.get("why_hire_this_person")}
    - Recruiter pitch: {resume_strategy.get("recruiter_pitch")}
    - Summary direction: {resume_strategy.get("summary_direction")}
    - Hard gaps: {resume_strategy.get("hard_gaps")}
    - Keywords to avoid overclaiming: {resume_strategy.get("keywords_to_avoid_overclaiming")}
    """

    prompt = f"""
    You are an elite resume strategist specializing in Product Manager positioning.

    Resume Writing Guide {WRITING_GUIDE}

    Write a concise, recruiter-quality professional summary for Ricardo Lugo.

    Your job:
    Write a summary that supports the winning story while staying strictly grounded in the selected candidate evidence.

    Winning story:
    {winning_story}

    Primary angle:
    {primary_angle}

    Secondary angle:
    {secondary_angle}

    Avoid angle:
    {avoid_angle}

    Why hire this person:
    {why_hire}

    Recruiter pitch:
    {recruiter_pitch}

    Summary direction:
    {summary_direction}

    Rewrite Guidance:
    {rewrite_focus}

    {strategy_text}

    Candidate evidence:
    {evidence}

    Rules:
    - Output ONLY the final summary.
    - Keep the summary under 45 words.
    - Use concise executive-level language.
    - Lead with the strongest credible positioning supported by the selected evidence.
    - The summary must explain why Ricardo is relevant for THIS role.
    - The summary must support the winning_story.
    - The primary_angle should guide the first sentence.
    - The secondary_angle may appear only if supported by the evidence.
    - Avoid reinforcing the avoid_angle.

    Evidence threshold rule:
    - Every major claim in the summary must be supported by selected achievements.
    - Do not use terminology that appears mainly in the job description but not in the candidate evidence.
    - Prefer evidence-derived positioning over keyword-derived positioning.
    - If a claim cannot be clearly traced to the selected evidence, do not use it.

    Positioning validation rule:

    - Treat the resume strategy as a positioning recommendation, not as a fact.
    - Before using target_positioning, winning_story, recruiter_pitch, or resume_narrative language, verify that the selected achievements provide direct evidence.
    - The stronger the claim, the stronger the evidence required.
    - If the positioning is only partially supported, qualify the language.
    - If the positioning is indirectly supported, emphasize transferable experience rather than direct ownership.
    - If the positioning is not supported by the selected achievements, downgrade to the nearest credible version.

    Examples:

    Direct evidence:
    Strategy recommends a platform product positioning and the selected achievements include platform roadmap ownership, platform launches, and platform adoption metrics.
    → Use the positioning confidently.

    Partial evidence:
    Strategy recommends a specialized positioning, but the selected achievements show adjacent experience.
    → Use qualified language and emphasize transferable strengths.

    Weak evidence:
    Strategy recommends a positioning that is not supported by the selected achievements.
    → Use broader positioning supported by the evidence.

    Credibility guardrails:
    - Do not claim direct ownership of copilots, agentic systems, LLM orchestration, ML platforms, recommendation engines, personalization systems, AI safety frameworks, evaluation pipelines, embedded systems, firmware, healthcare, AEC, 3D visualization, or generative design unless clearly supported by selected evidence.
    - Do not use phrases like "deep expertise", "expert in", "specialist in", or "proven success" unless strongly supported.
    - Prefer credible phrases such as:
    "experience building",
    "hands-on experience with",
    "worked across",
    "partnered with",
    "built adjacent systems",
    "applied AI-enabled workflows".

    Claim strength rule:
    - Match the strength of each claim to the maturity of the evidence.
    - Completed, measured outcomes can support strong language such as "led", "launched", "owned", "scaled", or "delivered."
    - Project-based, internal, consulting-based, or early-stage work should use language such as "built", "designed", "developed", "created", or "hands-on experience with."
    - Treat success_metrics as intended measurement criteria, not achieved outcomes.
    - Do not convert design goals, target metrics, expected outcomes, or success metrics into achieved results.
    

    AI wording rules:
    - Use "OpenAI API workflows" only if OpenAI appears in the selected evidence.
    - Use "AI-enabled workflows" only if AI/OpenAI appears in the selected evidence.
    - Do not use "agentic", "copilot", "LLM orchestration", "recommendation system", or "AI platform" unless those exact capabilities are supported by selected evidence.
    - If the evidence shows AI applied to automation or decision support, say "AI-enabled workflows" or "decision-support tools", not "copilot" or "agentic product."

    Style rules:
    - Avoid vague generic PM language.
    - Avoid buzzword stuffing.
    - Avoid long comma-separated capability lists.
    - Prefer one cohesive positioning narrative.
    - Prioritize credibility over aggressive positioning.
    - Do not overfit the summary to niche domain terminology if Ricardo does not have direct experience in that domain.
    """
    return call_openai(prompt).strip()