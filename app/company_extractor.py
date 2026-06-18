import re


def extract_company_name(job_text: str) -> str:
    patterns = [
        r"About Us\s+([A-Z][A-Za-z0-9&.\-\s]+?)\s+is\b",
        r"About\s+([A-Z][A-Za-z0-9&.\-\s]+)",
        r"at\s+([A-Z][A-Za-z0-9&.\-\s]+)\.",
        r"Join\s+([A-Z][A-Za-z0-9&.\-\s]+)",
        r"([A-Z][A-Za-z0-9&.\-\s]+)\s+is seeking",
        r"([A-Z][A-Za-z0-9&.\-\s]+)\s+is searching"
    ]

    for pattern in patterns:
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            company = re.sub(r"\s+", " ", company)
            company = company.replace("About Us", "").strip()
            return company

    return ""