import json
import re

from app.llm_client import call_openai


FIT_DIMENSIONS = {
    "domain_match": 0.20,
    "technical_match": 0.20,
    "product_match": 0.20,
    "industry_complexity_match": 0.10,
    "leadership_match": 0.10,
    "execution_match": 0.10,
    "tooling_match": 0.05,
    "education_match": 0.05,
}


def classify_fit(score: float) -> str:
    if score >= 9:
        return "Exceptional Fit"
    if score >= 8:
        return "Strong Fit"
    if score >= 7:
        return "Good Fit"
    if score >= 6:
        return "Stretch Fit"
    return "Weak Fit"


def calculate_weighted_score(dimension_scores: dict) -> float:
    total = 0

    for dimension, weight in FIT_DIMENSIONS.items():
        score = dimension_scores.get(dimension, 0)
        total += score * weight

    return round(total, 1)


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in LLM response.")

    return json.loads(match.group(0))


def analyze_role_fit(parsed_job: dict, selected_achievements: list) -> dict:
    evidence = []

    for ach in selected_achievements[:10]:
        evidence.append({
            "company": ach.get("company"),
            "title": ach.get("title"),
            "description": ach.get("description"),
            "metrics": ach.get("metrics"),
            "keywords": ach.get("keywords"),
            "strategic_category": ach.get("strategic_category"),
        })

    prompt = f"""
You are an experienced Product Management recruiter and hiring strategist.

Evaluate Ricardo Lugo's fit for the target role using a realistic, evidence-based scoring model.

Score each dimension from 0 to 10:
- 10 = excellent direct match
- 8 = strong transferable/direct match
- 6 = partial but credible match
- 4 = weak or indirect match
- 2 = minimal evidence
- 0 = no evidence

Dimensions:
1. domain_match: direct relevance to the company's industry/domain.
2. technical_match: match with required technical environment, systems, AI, APIs, analytics, data, or engineering context.
3. product_match: product ownership, roadmap, requirements, discovery, prioritization, product vision.
4. industry_complexity_match: experience with complex, physical-world, operational, industrial, logistics, IoT, or multi-stakeholder environments.
5. leadership_match: cross-functional leadership, stakeholder management, team coordination.
6. execution_match: evidence of delivery, implementation, launches, measurable business outcomes.
7. tooling_match: match with named tools, platforms, APIs, AI tools, analytics tools, cloud, or data stack.
8. education_match: degree alignment and education relevance.

Important evaluation principles:
- Be realistic, not overly optimistic.
- Do not automatically say Good Fit.
- Evaluate competitive strength, not just ability to apply.
- Penalize direct gaps, but distinguish between critical gaps and learnable gaps.
- Adjacent technical or operational experience should count positively when relevant.
- Applied AI workflow and automation experience should count positively, but do not treat it as equivalent to enterprise-scale AI/ML platform shipping.
- Weight execution, ownership, systems thinking, and stakeholder management heavily.
- If the role is AI-native, evaluate whether the candidate has hands-on AI building experience.
- If the role is logistics, supply chain, fulfillment, or physical operations, evaluate whether the candidate has relevant operational/physical-world experience.

Return ONLY valid JSON using this exact structure:

{{
  "dimension_scores": {{
    "domain_match": 0,
    "technical_match": 0,
    "product_match": 0,
    "industry_complexity_match": 0,
    "leadership_match": 0,
    "execution_match": 0,
    "tooling_match": 0,
    "education_match": 0
  }},
  "strengths": [
    "strength 1",
    "strength 2",
    "strength 3"
  ],
  "gaps": [
    "gap 1",
    "gap 2"
  ],
  "critical_gaps": [
    "critical gap if any"
  ],
  "learnable_gaps": [
    "learnable gap if any"
  ],
  "competitive_positioning": "One concise sentence explaining how Ricardo compares against likely candidates.",
  "positioning_advice": "Concise recruiter-style advice for how Ricardo should position himself."
}}

Parsed job:
{json.dumps(parsed_job, indent=2)}

Candidate evidence:
{json.dumps(evidence, indent=2)}
"""

    raw_response = call_openai(prompt)
    result = extract_json(raw_response)

    dimension_scores = result.get("dimension_scores", {})
    fit_score = calculate_weighted_score(dimension_scores)
    fit_level = classify_fit(fit_score)

    result["fit_score"] = fit_score
    result["fit_level"] = fit_level
    result["worth_applying"] = "Yes" if fit_score >= 7 else "Maybe" if fit_score >= 6 else "No"

    return result