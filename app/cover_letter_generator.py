from app.llm_client import call_openai
from app.company_extractor import extract_company_name


def generate_cover_letter(
    job_text: str,
    parsed_job: dict,
    selected_achievements: list,
    company_name: str = "",
    company_research: str = "",
    hiring_manager: str = "",
    tone: str = "human"
) -> str:
    if not company_name.strip():
        company_name = extract_company_name(job_text)

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

    recipient = hiring_manager.strip() if hiring_manager.strip() else "Hiring Team"

    prompt = f"""
You are helping Ricardo Lugo write a cover letter.

Write a concise, human-sounding cover letter tailored to the company and job.

Rules:
- Do not invent facts, metrics, tools, companies, or experience.
- Use only the job description, company research, and candidate evidence provided.
- Make it sound natural, direct, and specific — not overly polished or corporate.
- Do not use generic phrases like "I am excited to apply", "dynamic company", "results-driven", or "proven track record".
- Do not repeat the resume.
- Explain why the company and role make sense for Ricardo.
- Connect Ricardo's experience to the company's needs.
- If the company is AI-focused, mention AI practically and honestly based on evidence.
- If the company is product/operations/analytics focused, emphasize systems thinking, customer value, execution, and measurable outcomes.
- Keep it between 250 and 350 words.
- Use first person.
- Output only the cover letter body.
- Do not include date, address, greeting, or signature.

Recipient:
{recipient}

Company:
{company_name}

Tone:
{tone}

Parsed job:
{parsed_job}

Job description:
{job_text}

Company research / notes:
{company_research}

Candidate evidence:
{evidence}
"""

    return call_openai(prompt).strip()