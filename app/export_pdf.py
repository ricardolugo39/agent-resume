import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.resume_generator import generate_resume_outline
from app.resume_renderer_html import render_resume_html


OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def save_resume_pdf(
    job_text: str,
    top_n: int = 10,
    filename: str | None = None,
    resume_strategy: dict | None = None,
    outline_override: dict | None = None
) -> Path:
    if outline_override:
        resume_data = outline_override
    else:
        resume_data = generate_resume_outline(
            job_text,
            top_n=top_n,
            resume_strategy=resume_strategy
        )

    html_content = render_resume_html(resume_data)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}.pdf"

    output_path = OUTPUT_DIR / filename

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        page.pdf(
            path=str(output_path),
            format="Letter",
            print_background=True,
            margin={
                "top": "0.55in",
                "right": "0.55in",
                "bottom": "0.55in",
                "left": "0.55in",
            },
        )
        browser.close()

    return output_path


if __name__ == "__main__":
    sample_job = """
    Product Manager responsible for IoT, APIs, analytics, Agile delivery,
    roadmap ownership, hardware/software collaboration, user stories,
    acceptance criteria, customer discovery, and platform integrations.
    """

    output_file = save_resume_pdf(sample_job, top_n=12)

    print(f"PDF exported to: {output_file}")