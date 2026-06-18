import json
from pathlib import Path
from html import escape


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def load_experiences():
    path = DATA_DIR / "experiences.json"

    with open(path, "r", encoding="utf-8") as f:
        experiences = json.load(f)

    return {
        exp["company"]: exp
        for exp in experiences
    }


def build_core_skills(resume_data: dict) -> str:
    parsed_job = resume_data.get("parsed_job", {})
    keywords = parsed_job.get("keywords", [])

    skill_map = {
        "api": "APIs",
        "apis": "APIs",
        "iot": "IoT Platforms",
        "telemetry": "Telemetry Analytics",
        "analytics": "Analytics",
        "forecasting": "Forecasting Systems",
        "agile": "Agile Delivery",
        "roadmap": "Roadmap Strategy",
        "automation": "Operational Automation",
        "hardware": "Hardware/Software Collaboration",
        "firmware": "Firmware Coordination",
        "customer discovery": "Customer Discovery",
        "user stories": "User Stories",
        "acceptance criteria": "Acceptance Criteria",
        "mixed assets": "Asset Operations",
        "operations": "Operational Systems", 
        "ai": "AI Product Management",
        "llm": "LLM Applications",
        "llms": "LLM Applications",
        "rag": "RAG Systems",
        "retrieval-augmented generation": "RAG Systems",
        "embeddings": "Embeddings",
        "vector search": "Vector Search",
        "human-in-the-loop": "Human-in-the-Loop AI",
        "evaluation": "AI Evaluation",
        "hallucination": "AI Quality"
    }

    selected = []

    preferred_order = [
    
        "Product Strategy",
        "AI Product Management",
        "RAG Systems",
        "LLM Applications",
        "AI Evaluation",
        "Human-in-the-Loop AI",
        "Vector Search",
        "Embeddings",
        "IoT Platforms",
        "APIs",
        "Telemetry Analytics",
        "Forecasting Systems",
        "Agile Delivery",
        "Roadmap Strategy",
        "Customer Discovery",
        "Hardware/Software Collaboration",
        "Operational Automation"
    ]
    

    for keyword in keywords:
        if keyword in skill_map:
            selected.append(skill_map[keyword])

    selected.append("Product Strategy")

    ordered = []

    for skill in preferred_order:
        if skill in selected:
            ordered.append(skill)

    return " • ".join(dict.fromkeys(ordered))


def clean_bullet(bullet: str) -> str:

    bullet = bullet.replace("with impact including", "")
    bullet = bullet.replace("  ", " ")

    bullet = bullet.strip()

    return bullet


def render_resume_html(resume_data: dict) -> str:

    summary = escape(resume_data.get("summary", ""))
    bullets_by_company = resume_data.get("bullets_by_company", {})

    experiences_map = load_experiences()

    core_skills = build_core_skills(resume_data)

    experience_html = ""

    for company, bullets in bullets_by_company.items():

        experience = experiences_map.get(company, {})

        role = experience.get("role", "")
        dates = experience.get("dates", "")

        bullet_html = "\n".join(
            f"<li>{escape(clean_bullet(bullet.lstrip('- ').strip()))}</li>"
            for bullet in bullets
        )

        experience_html += f"""
        <section class="job">

            <div class="job-header">
                <div class="job-company">{escape(company)}</div>
                <div class="job-role">{escape(role)} | {escape(dates)}</div>
            </div>

            <ul>
                {bullet_html}
            </ul>

        </section>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Ricardo Lugo Resume</title>

<style>

    @page {{
        size: Letter;
        margin: 0.55in;
    }}

    body {{
        font-family: Arial, Helvetica, sans-serif;
        color: #111;
        font-size: 10.2pt;
        line-height: 1.35;
    }}

    .header {{
        text-align: center;
        margin-bottom: 16px;
    }}

    .name {{
        font-size: 22pt;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    .contact {{
        font-size: 9pt;
        margin-top: 4px;
        color: #333;
    }}

    h1 {{
        font-size: 11pt;
        border-bottom: 1px solid #222;
        padding-bottom: 3px;
        margin-top: 16px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .summary {{
        margin-bottom: 6px;
    }}

    .skills {{
        margin-top: 4px;
        margin-bottom: 10px;
        line-height: 1.5;
    }}

    .job {{
        margin-bottom: 12px;
    }}

    .job-header {{
        margin-bottom: 4px;
    }}

    .job-company {{
        font-size: 10.5pt;
        font-weight: 700;
        text-transform: uppercase;
    }}

    .job-role {{
        font-size: 9.5pt;
        color: #444;
        margin-top: 1px;
    }}

    ul {{
        margin-top: 4px;
        margin-bottom: 4px;
        padding-left: 18px;
    }}

    li {{
        margin-bottom: 4px;
    }}

</style>

</head>

<body>

    <div class="header">
        <div class="name">RICARDO LUGO</div>

        <div class="contact">
            +1(954)253-6048 | ricardolugo39@me.com | Pembroke Pines, FL |
            linkedin.com/in/ricardo-lugo
        </div>  
    </div>

    <h1>Summary</h1>

    <div class="summary">
        {summary}
    </div>

    <h1>Core Skills</h1>

    <div class="skills">
        {escape(core_skills)}
    </div>

    <h1>Technical Tools</h1>

<div class="skills">
    Python • SQL • Power BI • Databricks • Streamlit • OpenAI APIs • Azure • SQLite • Jira • Confluence
</div>

    <h1>Experience</h1>

    {experience_html}

    <h1>Education</h1>

<section class="job">

    <div class="job-header">
        <div class="job-company">
            Florida International University
        </div>

        <div class="job-role">
            Master of Business Administration (MBA) | 2018
        </div>
    </div>

</section>

<section class="job">

    <div class="job-header">
        <div class="job-company">
            Florida International University
        </div>

        <div class="job-role">
            Bachelor of Science (BS) in Mechanical Engineering | 2010
        </div>
    </div>

</section>

</body>
</html>
"""