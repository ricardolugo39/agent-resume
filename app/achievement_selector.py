import json
import re

from app.llm_client import call_openai


def extract_json_list(text: str) -> list[str]:
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "selected_ids" in data:
            return data["selected_ids"]
    except Exception:
        pass

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        return []

    try:
        return json.loads(match.group(0))
    except Exception:
        return []


def select_achievements_with_strategy(
    achievements: list[dict],
    resume_strategy: dict,
    top_n: int = 12
) -> list[dict]:

    compact_achievements = []

    for ach in achievements:
        compact_achievements.append({
            "id": ach.get("id"),
            "company": ach.get("company"),
            "title": ach.get("title"),
            "description": ach.get("description"),
            "business_problem": ach.get("business_problem"),
            "solution": ach.get("solution"),
            "business_impact": ach.get("business_impact"),
            "metrics": ach.get("metrics"),
            "keywords": ach.get("keywords"),
            "match_score": ach.get("match_score"),
            "evidence_type": ach.get("evidence_type"),
            "secondary_evidence_types": ach.get("secondary_evidence_types", []),
        })

    winning_story = resume_strategy.get("winning_story", "")
    primary_angle = resume_strategy.get("primary_angle", "")
    secondary_angle = resume_strategy.get("secondary_angle", "")
    avoid_angle = resume_strategy.get("avoid_angle", "")
    why_hire = resume_strategy.get("why_hire_this_person", "")

    prompt = f"""
You are selecting resume achievements for Ricardo Lugo.

Candidate story to prove:
{resume_strategy.get("winning_story", "")}

Primary angle:
{resume_strategy.get("primary_angle", "")}

Secondary angle:
{resume_strategy.get("secondary_angle", "")}

Avoid angle:
{resume_strategy.get("avoid_angle", "")}

Why hire this person:
{resume_strategy.get("why_hire_this_person", "")}

Recruiter pitch:
{resume_strategy.get("recruiter_pitch", "")}

Preferred evidence types:
{resume_strategy.get("preferred_evidence_types", [])}

Avoid evidence types:
{resume_strategy.get("avoid_evidence_types", [])}

Return ONLY valid JSON:
{{
  "selected_ids": ["achievement_id_1", "achievement_id_2"]
}}

Selection hierarchy:

1. Proves winning_story
2. Supports primary_angle
3. Strengthens secondary_angle
4. Avoids avoid_angle
5. Covers important role dimensions
6. Maintains evidence diversity
7. Keyword relevance

Selection rules:

- Select exactly {top_n} achievements if enough strong options exist.
- The selected achievements must prove the winning story.
- Prioritize evidence supporting the primary angle.
- Use the secondary angle only to strengthen credibility.
- Avoid achievements that reinforce the avoid angle.
- Prioritize achievements whose evidence_type or secondary_evidence_types match preferred_evidence_types.
- Avoid achievements whose evidence_type or secondary_evidence_types match avoid_evidence_types unless they are essential to proving the winning_story.
- If the JD is for a platform, dashboard, portal, workflow, UX, personalization, or information architecture role, prioritize platform strategy, roadmap ownership, UX, adoption, customer discovery, and stakeholder influence over analytics/reporting achievements.

Evidence diversity requirements:

- Prefer a mix of evidence types.
- Avoid selecting more than 2 achievements from the same evidence_type unless the role strongly requires it.
- Do not let analytics, reporting, dashboards, forecasting, inventory planning, or operational reporting dominate unless the JD explicitly prioritizes them.
- Avoid selecting multiple achievements that essentially tell the same story.

Target evidence mix when possible:

The target evidence mix is guidance, not a quota.

Do not force evidence diversity if it weakens the story.

A coherent hiring narrative is more important than perfectly balanced evidence categories.

- platform_strategy
- roadmap_ownership
- customer_discovery
- ux
- adoption
- experimentation
- stakeholder_influence
- business_outcomes
- technical_delivery

Selection philosophy:

- Do not select achievements simply because they have the highest keyword overlap.
- Do not select achievements simply because they have strong metrics.
- Do not select achievements simply because they scored highly in ranking.
- Treat match_score only as a signal, not the decision.
- Treat evidence_type as an important signal.

Ask yourself:

"If I were presenting Ricardo to a hiring manager for THIS role, which achievements would most convincingly support the story?"

Select the evidence that would most likely earn an interview.

Resume strategy:
{json.dumps(resume_strategy, indent=2)}

Candidate achievements:
{json.dumps(compact_achievements, indent=2)}
"""

    raw = call_openai(prompt)
    selected_ids = extract_json_list(raw)

    selected_id_set = set(selected_ids)

    selected = [
        ach for ach in achievements
        if ach.get("id") in selected_id_set
    ]

    selected_sorted = []

    for selected_id in selected_ids:
        for ach in selected:
            if ach.get("id") == selected_id:
                selected_sorted.append(ach)
                break

    if len(selected_sorted) < top_n:
        for ach in achievements:
            if ach.get("id") not in selected_id_set:
                selected_sorted.append(ach)
                selected_id_set.add(ach.get("id"))

            if len(selected_sorted) >= top_n:
                break

    return selected_sorted[:top_n]