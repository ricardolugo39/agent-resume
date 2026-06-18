from app.matcher import match_achievements


def analyze_keyword_coverage(job_text: str, top_n: int = 10) -> dict:
    results = match_achievements(job_text, top_n=top_n)

    job_keywords = set(results["parsed_job"].get("keywords", []))
    matched_keywords = set()

    for achievement in results["top_achievements"]:
        matched_keywords.update(achievement.get("matched_keywords", []))

    missing_keywords = sorted(job_keywords - matched_keywords)
    covered_keywords = sorted(job_keywords & matched_keywords)

    coverage_rate = 0
    if job_keywords:
        coverage_rate = round(len(covered_keywords) / len(job_keywords), 2)

    return {
        "job_keywords": sorted(job_keywords),
        "covered_keywords": covered_keywords,
        "missing_keywords": missing_keywords,
        "coverage_rate": coverage_rate
    }


if __name__ == "__main__":
    sample_job = """
    Senior Product Manager responsible for APIs, analytics,
    SQL reporting, forecasting, Agile delivery, customer discovery,
    and platform integrations.
    """

    print(analyze_keyword_coverage(sample_job))