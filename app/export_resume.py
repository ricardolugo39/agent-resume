import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from datetime import datetime

from app.resume_generator import generate_resume_outline


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


NAME = "Ricardo Lugo"

CONTACT_INFO = [
    "+1(954)253-6048",
    "ricardolugo39@me.com",
    "Pembroke Pines, FL",
    "linkedin.com/in/ricardo-lugo"
]


def format_header():
    lines = [
        NAME.upper(),
        " | ".join(CONTACT_INFO),
        "=" * 80
    ]

    return "\n".join(lines)


def format_summary(summary: str):
    return f"""
SUMMARY
--------------------------------------------------------------------------------
{summary}
"""


def format_company_section(company: str, bullets: list):
    lines = [
        f"""
{company.upper()}
--------------------------------------------------------------------------------
"""
    ]

    for bullet in bullets:
        lines.append(bullet)

    return "\n".join(lines)


def build_resume_markdown(job_text: str, top_n: int = 10):
    outline = generate_resume_outline(job_text, top_n=top_n)

    sections = []

    sections.append(format_header())
    sections.append(format_summary(outline["summary"]))

    sections.append("""
EXPERIENCE
================================================================================
""")

    for company, bullets in outline["bullets_by_company"].items():
        sections.append(
            format_company_section(company, bullets)
        )

    return "\n".join(sections)


def save_resume_markdown(content: str, filename: str = None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}.md"

    output_path = OUTPUT_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


if __name__ == "__main__":

    sample_job = """
    Senior Product Manager responsible for APIs, analytics,
    SQL reporting, forecasting, Agile delivery, customer discovery,
    IoT, hardware/software collaboration, roadmap ownership,
    and platform integrations.
    """

    resume = build_resume_markdown(sample_job)

    output_file = save_resume_markdown(resume)

    print(f"\nResume exported to:\n{output_file}")