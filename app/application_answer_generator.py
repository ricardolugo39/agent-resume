from app.llm_client import call_openai


def generate_application_answer(
    question: str,
    job_text: str,
    parsed_job: dict,
    selected_achievements: list,
    company_name: str = "",
    answer_length: str = "medium"
) -> str:
    evidence = []

    for ach in selected_achievements[:10]:
        evidence.append({
            "company": ach.get("company"),
            "title": ach.get("title"),
            "description": ach.get("description"),
            "business_problem": ach.get("business_problem"),
            "solution": ach.get("solution"),
            "business_impact": ach.get("business_impact"),
            "metrics": ach.get("metrics"),
            "keywords": ach.get("keywords"),
            "strategic_category": ach.get("strategic_category")
        })

    length_guidance = {
        "short": "Keep the answer under 120 words.",
        "medium": "Keep the answer between 150 and 220 words.",
        "long": "Keep the answer between 250 and 350 words."
    }.get(answer_length, "Keep the answer between 150 and 220 words.")

    prompt = f"""
You are helping Ricardo Lugo answer an application question.

Write a strong, specific, human-sounding answer tailored to the company, role, and question.

Rules:
- Do not invent facts, metrics, companies, tools, or experience.
- Use only the candidate evidence provided.
- Answer the exact question directly.
- Tailor the answer to the job description and company context.
- If the role is AI-focused, make the answer AI-aware and practical, not buzzword-heavy.
- Use Ricardo's real positioning: Product Manager with experience in analytics, operational systems, AI workflows, IoT/platform work, and customer-facing technical environments.
- Sound natural, confident, and specific.
- Avoid corporate clichés like "I am passionate about", "fast-paced environment", "dynamic", or "results-driven".
- Do not exaggerate AI/ML experience beyond the evidence.
- Use first person.
- {length_guidance}
- Output only the answer.

Company:
{company_name}

Application question:
{question}

Parsed job:
{parsed_job}

Job description:
{job_text}

Candidate evidence:
{evidence}
"""

    return call_openai(prompt).strip()