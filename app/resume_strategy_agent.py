import json
import re

from app.llm_client import call_openai


RICARDO_PROFILE = """
Ricardo Lugo profile:
- MBA, Florida International University
- BS Mechanical Engineering, Florida International University
- Product Manager experience across analytics, APIs, IoT, operational systems, automation, e-commerce, and industrial products.
- Tools: Python, SQL, Power BI, OpenAI APIs, RAG, embeddings, vector search, AI evaluation frameworks, Streamlit, Hugging Face, Azure, Snowflake, Databricks, Google Analytics, Shopify, Amazon Seller Central.
- LITET: built AI-powered analytics agents, automated sales/PPC/inventory reporting, grew e-commerce revenue, improved ROAS, built inventory forecasting and operational tools.
- Independent AI & Product Consulting: building and designing RAG-based knowledge assistants, AI evaluation frameworks, and workflow automation concepts for industrial product teams, including technical documentation retrieval and competitor-to-THK interchange workflows.
- Emerson: Product Manager for analytics and API platforms, telemetry analytics, REST APIs, enterprise reporting, data delivery, Snowflake/Azure/data workflows.
- Chamberlain: Software Product Manager for MyQ platform, IoT product delivery, cross-functional work across software, firmware, hardware, UX, analytics, RICE prioritization, Agile.
- Lugo Hermanos: industrial product/branch leadership, inventory planning, forecasting, vendor negotiation, industrial automation, THK/Thomson linear motion.
- Regal Rexnord: industrial sales/account management, OEM accounts, technical product adoption, customer training.
"""


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in strategy response.")

    return json.loads(match.group(0))


def build_resume_strategy_from_jd(
    job_description: str,
    candidate_fit: dict,
    selected_achievements: list | None = None
) -> dict:
    evidence_text = (
        json.dumps(selected_achievements[:15], indent=2)
        if selected_achievements
        else "[]"
    )

    json_schema = """
    {
    "proven_identity": "Most defensible evidence-based identity",

    "adjacent_identity": "Supporting adjacent capability",

    "target_positioning": "Concise role-specific positioning title",

    "winning_story": "The single story the resume must prove",

    "primary_angle": "Main reason this candidate should be hired",

    "secondary_angle": "Supporting angle that strengthens the case",

    "avoid_angle": "Story the resume should avoid accidentally telling",

    "why_hire_this_person": "Direct hiring rationale",

    "recruiter_pitch": "One sentence a recruiter would tell a hiring manager",

    "resume_narrative": "One sentence explaining the overall resume story",

    "positioning_confidence": {
        "proven_identity": "high | medium | low",
        "adjacent_identity": "high | medium | low",
        "target_positioning": "high | medium | low",
        "winning_story": "high | medium | low",
        "reason": "Why this positioning is well supported",
        "largest_risk": "Most likely positioning overstatement"
    },

    "role_dimensions": [
        {
        "dimension": "Specific capability required by the JD",
        "importance": 0.0,
        "candidate_match": "strong | moderate | weak | gap",
        "evidence_to_use": [
            "specific Ricardo evidence"
        ],
        "risk": "specific positioning risk or null"
        }
    ],

    "selection_priorities": [],

    "preferred_evidence_types": [],

    "avoid_evidence_types": [],

    "experiences_to_prioritize": [],

    "experiences_to_deprioritize": [],

    "keywords_to_include": [],

    "keywords_to_avoid_overclaiming": [],

    "summary_direction": "",

    "bullet_strategy": "",

    "experience_order_strategy": "",

    "tone": "",

    "positioning_advice": ""
    }
    """


    prompt = f"""
You are an elite executive resume strategist.

Your responsibility is NOT to evaluate the candidate.

A Candidate Fit assessment has already been completed.

Treat the Candidate Fit Assessment as established fact.

Do NOT:

- Re-evaluate candidate fit.
- Determine whether Ricardo should apply.
- Identify new hard gaps.
- Contradict the Candidate Fit assessment.
- Recommend positioning that exceeds the evidence.

Your responsibility is to transform the Candidate Fit Assessment into the strongest truthful resume strategy.

Candidate Fit Assessment

{json.dumps(candidate_fit, indent=2)}

Return ONLY valid JSON.

Required JSON structure:

{json_schema}

Positioning rules:

1. The proven_identity must be derived ONLY from selected achievement evidence.

2. The adjacent_identity may use transferable or adjacent experience.

3. The target_positioning must be explainable as:

    proven_identity
    +
    adjacent_identity

4. Do not elevate adjacent experience into the primary identity unless the evidence clearly supports it.

5. The job description may influence wording but may not replace the proven identity.

6. The winning_story must reinforce the Candidate Fit assessment.

7. The primary_angle should emphasize the strongest reason Ricardo should receive an interview.

8. The secondary_angle should strengthen the primary story without changing it.

9. The avoid_angle should describe the misleading narrative the resume must avoid.

10. The recruiter_pitch should summarize why a recruiter should advance Ricardo to the hiring manager.

11. The resume_narrative should provide one coherent story that all sections of the resume support.

Evidence strategy:

- preferred_evidence_types should prioritize the evidence that best supports the winning_story.

- avoid_evidence_types should identify evidence that could unintentionally weaken the positioning.

- Do not over-select analytics, dashboards, reporting, forecasting, or operational tooling unless they directly support the winning_story.

- Prefer platform ownership, product strategy, customer discovery, roadmap ownership, business outcomes, adoption, experimentation, technical delivery, and stakeholder influence when supported by evidence.

Experience prioritization:

Recommend:

- experiences_to_prioritize

- experiences_to_deprioritize

based on the strongest interview narrative.

Role dimensions:

For every important capability required by the job:

- estimate its importance

- identify the strongest evidence to support it

- identify any positioning risk

Do not invent evidence.

Scoring guidance:

- Confidence should reflect how well the selected evidence supports the positioning.

- largest_risk should describe the greatest over-positioning risk.

Be conservative.

Optimize for interview probability, not keyword overlap.

Ricardo Profile:

{RICARDO_PROFILE}

Selected Achievement Evidence:

{evidence_text}

Job Description:

{job_description}
"""

    raw = call_openai(prompt)
    strategy = extract_json(raw)

    total_importance = sum(
        d.get("importance", 0)
        for d in strategy.get("role_dimensions", [])
    )

    if total_importance > 0:
        for d in strategy["role_dimensions"]:
            d["importance"] = round(d.get("importance", 0) / total_importance, 3)

    strategy.setdefault("preferred_evidence_types", [])
    strategy.setdefault("avoid_evidence_types", [])
    strategy.setdefault("positioning_confidence", {
        "proven_identity": "medium",
        "adjacent_identity": "medium",
        "target_positioning": "medium",
        "winning_story": "medium",
        "reason": "",
        "largest_risk": ""
    })

    return strategy