import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.cover_letter_renderer_html import render_cover_letter_html


OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def save_cover_letter_pdf(
    cover_letter: str,
    company_name: str = "",
    hiring_manager: str = "",
    filename: str | None = None
) -> Path:
    html_content = render_cover_letter_html(
        cover_letter=cover_letter,
        company_name=company_name,
        hiring_manager=hiring_manager
    )

    if filename is None:
        safe_company = company_name.lower().replace(" ", "_") if company_name else "company"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cover_letter_{safe_company}_{timestamp}.pdf"

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
                "top": "0.75in",
                "right": "0.75in",
                "bottom": "0.75in",
                "left": "0.75in",
            },
        )
        browser.close()

    return output_path