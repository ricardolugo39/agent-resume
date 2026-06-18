from html import escape
from datetime import date


def render_cover_letter_html(
    cover_letter: str,
    company_name: str = "",
    hiring_manager: str = ""
) -> str:
    recipient = hiring_manager.strip() if hiring_manager.strip() else "Hiring Team"
    company_line = company_name.strip() if company_name.strip() else ""

    paragraphs = [
        p.strip()
        for p in cover_letter.split("\n")
        if p.strip()
    ]

    paragraphs_html = "\n".join(
        f"<p>{escape(p)}</p>"
        for p in paragraphs
    )

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Ricardo Lugo Cover Letter</title>

<style>
    @page {{
        size: Letter;
        margin: 0.75in;
    }}

    body {{
        font-family: Arial, Helvetica, sans-serif;
        color: #111;
        font-size: 10.5pt;
        line-height: 1.45;
    }}

    .header {{
        text-align: center;
        margin-bottom: 24px;
    }}

    .name {{
        font-size: 20pt;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    .contact {{
        font-size: 9pt;
        margin-top: 4px;
        color: #333;
    }}

    .date {{
        margin-bottom: 20px;
    }}

    .recipient {{
        margin-bottom: 20px;
    }}

    p {{
        margin-bottom: 12px;
    }}

    .signature {{
        margin-top: 24px;
    }}
</style>
</head>

<body>

    <div class="header">
        <div class="name">RICARDO LUGO</div>
        <div class="contact">
            +1 (954) 253-6048 | ricardolugo39@me.com | Pembroke Pines, FL |
            linkedin.com/in/ricardo-lugo
        </div>
    </div>

    <div class="date">{date.today().strftime("%B %d, %Y")}</div>

    <div class="recipient">
        {escape(recipient)}<br>
        {escape(company_line)}
    </div>

    {paragraphs_html}

    <div class="signature">
        Sincerely,<br>
        Ricardo Lugo
    </div>

</body>
</html>
"""