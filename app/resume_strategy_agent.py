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

    "resume_narrative": "One sentence explaining the resume story",

    "positioning_confidence": {
        "proven_identity": "high | medium | low",
        "adjacent_identity": "high | medium | low",
        "target_positioning": "high | medium | low",
        "winning_story": "high | medium | low",
        "reason": "Brief explanation of how directly the selected evidence supports the positioning",
        "largest_risk": "Most likely overstatement risk"
    },

    "role_dimensions": [
        {
        "dimension": "Specific capability required by the JD",
        "importance": 0.0,
        "candidate_match": "strong | moderate | weak | gap",
        "evidence_to_use": ["specific Ricardo evidence"],
        "risk": "specific risk or null"
        }
    ],

    "selection_priorities": [],

    "preferred_evidence_types": [
        "evidence types that best prove the winning_story"
    ],

    "avoid_evidence_types": [
        "evidence types that would misframe the candidate for this role"
    ],

    "experiences_to_prioritize": [],

    "experiences_to_deprioritize": [],

    "primary_strengths": [],

    "credible_adjacencies": [],

    "hard_gaps": [],

    "keywords_to_include": [],

    "keywords_to_avoid_overclaiming": [],

    "summary_direction": "",

    "bullet_strategy": "",

    "tone": "",

    "fit_level": "",

    "fit_score": 0.0,

    "positioning_advice": ""
    }
"""

    prompt = f"""
You are a senior Product Management recruiter, hiring manager, and resume positioning strategist.

Your job is to create a role-specific resume strategy for Ricardo Lugo based on the job description.

Do NOT force the role into fixed categories like AI PM, Growth PM, Operations PM, or Technical PM.
Do NOT default to Ricardo's strongest recurring themes such as analytics, dashboards, forecasting, reporting, or operational automation unless the JD truly calls for them.

Your most important task is to answer:

"What is the strongest evidence-backed story Ricardo can credibly tell for THIS role?"

Think like a recruiter preparing a candidate presentation to a hiring manager.

Evidence-first positioning rule:

The resume strategy must be derived from Ricardo's evidence first and the job description second.

Do not create a story from the job description and then search for supporting evidence.

Instead:

1. Determine what the selected evidence directly proves.
2. Determine which role requirements are directly supported.
3. Determine which role requirements are adjacent or transferable.
4. Build the strongest credible positioning from that analysis.

The goal is not maximum fit.

The goal is maximum credibility.

A slightly weaker but fully supported positioning is better than a stronger positioning that requires assumptions.

The target_positioning, winning_story, recruiter_pitch, and resume_narrative must describe what the evidence proves, not what the job description wishes existed.

Before selecting achievements, determine:

1. What is the single strongest story this candidate can credibly tell?
2. What is the primary hiring angle?
3. What is the secondary supporting angle?
4. What misleading story should the resume avoid?
5. What would a recruiter say when presenting this candidate to a hiring manager?

Produce:

- winning_story
- primary_angle
- secondary_angle
- avoid_angle
- why_hire_this_person
- recruiter_pitch

These fields are critical because they will drive achievement selection and resume generation.

Step 1: Understand the role
- What is the company actually hiring for?
- What problem will this person own?
- What capabilities matter most?
- What would make a candidate stand out?

Step 2: Separate role needs from Ricardo's default strengths
- Do not let analytics, dashboards, reporting, forecasting, or operations dominate unless they are central to the JD.
- Identify when those capabilities should be reframed as platform thinking, customer insight, product strategy, experimentation, systems thinking, customer experience, or workflow simplification.

Step 3: Build the candidate story

Before defining the winning story:

A. Identify Direct Evidence
- What capabilities are clearly demonstrated by the selected achievements?
- What outcomes are clearly supported?
- What responsibilities were clearly owned?

B. Identify Transferable Evidence
- Which capabilities are adjacent to the role?
- Which experiences increase credibility without being direct matches?

C. Identify Unsupported Areas
- Which role requirements are weakly supported or not supported?

Identity derivation step:

Before generating target_positioning, determine:

1. proven_identity
   - What is Ricardo most clearly proven to be based on the selected evidence?
   - This should be evidence-first.
   - Ignore the job title when answering.
   - Use the strongest identity that can be directly defended from the achievements.

2. adjacent_identity
   - What adjacent capability strengthens the fit?
   - This may come from consulting work, AI projects, domain expertise, platform work, technical depth, or transferable experience.
   - Adjacent identity should complement the proven identity, not replace it.

Examples:

Proven:
Enterprise Platform Product Manager

Adjacent:
AI workflow and RAG-based product development

---

Proven:
Technical Product Manager

Adjacent:
Enterprise analytics and API products

---

Proven:
Product Manager

Adjacent:
Applied AI workflow development

Target positioning rule:

target_positioning must be derived from proven_identity first.

The target_positioning should generally follow:

[proven_identity]

or

[proven_identity] with [adjacent_identity]

Do not elevate adjacent_identity into the primary identity unless the evidence strongly supports it.

The job description may influence wording, but may not replace the proven identity.

Only after completing those three steps should you define:

- winning_story
- primary_angle
- secondary_angle
- recruiter_pitch
- resume_narrative

The winning_story must be grounded primarily in direct evidence.

Transferable evidence may strengthen the story but should not become the story.

Unsupported requirements should appear as gaps, not as positioning.

Combination claim rule:

Do not combine separate experiences into a stronger claim unless the evidence directly supports the combined claim.

Do not merge two separate bodies of evidence into one stronger combined claim unless the selected achievements directly support that combined claim.

If the candidate has one set of achievements showing Capability A and another set showing Capability B, the positioning should usually be:

"Capability A with experience in Capability B"

not:

"Capability A+B leader"

When in doubt, prefer:

"[Primary proven identity] with [adjacent experience]"

Examples:

Platform Product Manager with hands-on AI workflow experience

Enterprise Product Manager with experience building RAG-based knowledge systems

Technical Product Manager with applied AI workflow development experience

These are often more credible than specialized AI titles.

Step 3B: Define evidence strategy
- Based on the winning_story, identify which evidence types should be prioritized.
- Populate preferred_evidence_types with the evidence categories that would best prove the story.
- Populate avoid_evidence_types with evidence categories that could misframe Ricardo or pull the resume away from the role.
- Do not choose evidence types based on fixed role labels.
- Choose evidence types based on the actual JD, winning_story, primary_angle, and avoid_angle.

Step 4: Evaluate fit honestly
- Identify direct matches.
- Identify credible adjacencies.
- Identify hard gaps.
- Do not invent domain expertise.
- Do not inflate fit because of keyword overlap.

Return ONLY valid JSON.

Required JSON structure:

{json_schema}

Scoring guidance:
- 9-10: Exceptional direct fit
- 8-8.9: Strong fit
- 7-7.9: Good fit
- 6-6.9: Stretch but worth applying
- Below 6: Weak fit

Important:

- Be honest and realistic.
- Do not invent domain expertise.
- Do not inflate positioning based on keyword overlap.
- The strategy should describe Ricardo's strongest proven identity, not the ideal candidate described by the job posting.

Identity rule:

- proven_identity must be derived only from selected evidence.
- adjacent_identity may use transferable or adjacent experience.
- target_positioning must be explainable as:
  proven_identity + adjacent_identity.
- If target_positioning cannot be explained through those two fields, it is too aggressive and should be downgraded.

AI-specific guidance:

- Applied AI workflows are valuable but are not the same as owning enterprise AI platforms.
- Building RAG systems is not automatically equivalent to owning AI products.
- Building internal AI tools is not automatically equivalent to enterprise AI platform leadership.
- AI workflow development should be positioned according to scope, ownership, adoption, and business impact.
- Use stronger AI positioning only when the evidence clearly demonstrates AI product ownership, launch responsibility, adoption, and measurable outcomes.
- If AI is mentioned, determine whether AI is the core product, an enabling feature, or a workflow accelerator. Position the candidate around the core business problem first and AI second when AI is not the entire product.


- Industrial, IoT, telemetry, operations, and e-commerce experience can be strong transferable evidence when relevant.
- If the role is a hybrid, describe the hybrid. Do not reduce it to one box.
- Avoid positioning Ricardo as an analytics/dashboard/reporting candidate unless that is truly the strongest story for the JD.
- preferred_evidence_types and avoid_evidence_types must be specific and useful for achievement selection.
- Do not default to analytics, automation, forecasting, or dashboards unless those directly support the winning_story.
- Prefer interview-winning narrative over keyword stuffing.
- The output should help downstream resume generation choose and frame achievements.
- For product roles involving dashboards, platforms, portals, UX, personalization, workflows, or information architecture, prioritize platform/product experience over pure analytics/reporting language.

Ricardo profile:
{RICARDO_PROFILE}

Selected achievement evidence:
{evidence_text}

Job description:
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