import json
from pathlib import Path
from rapidfuzz import fuzz

from app.job_parser import parse_job_description


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


ROLE_COMPANY_WEIGHTS = {
    "technical_pm": {
        "Chamberlain Group": 15,
        "Emerson Electric": 14,
        "Independent AI & Product Consulting": 12,
        "LITET": 10,
        "Lugo Hermanos": 4,
        "Regal Rexnord": 3
    },
    "data_pm": {
        "LITET": 15,
        "Emerson Electric": 14,
        "Independent AI & Product Consulting": 12,
        "Chamberlain Group": 12,
        "Lugo Hermanos": 5,
        "Regal Rexnord": 3
    },
    "ai_pm": {
        "LITET": 18,
        "Independent AI & Product Consulting": 18,
        "Emerson Electric": 8,
        "Chamberlain Group": 6
    },
    "operations_pm": {
        "LITET": 15,
        "Lugo Hermanos": 12,
        "Regal Rexnord": 9,
        "Emerson Electric": 5
    },
    "industrial_pm": {
        "Lugo Hermanos": 15,
        "Regal Rexnord": 14,
        "Emerson Electric": 10,
        "Chamberlain Group": 4
    },
    "growth_pm": {
        "LITET": 18,
        "Emerson Electric": 6,
        "Chamberlain Group": 5
    }, 
    
}


ROLE_MAP = {
    "technical_pm": ["technical pm", "platform pm", "api pm", "iot pm", "product manager"],
    "data_pm": ["data pm", "analytics pm", "product manager"],
    "ai_pm": ["ai pm", "technical pm", "data pm"],
    "operations_pm": ["operations pm", "supply chain pm", "technical pm"],
    "industrial_pm": ["industrial pm", "technical pm", "product manager"],
    "growth_pm": ["growth pm", "e-commerce pm", "product manager"]
}


def load_json(filename: str):
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(text: str) -> str:
    return str(text).lower().strip()


def build_achievement_text(achievement: dict) -> str:
    return normalize(
        " ".join([
            achievement.get("title", ""),
            achievement.get("description", ""),
            achievement.get("business_problem", ""),
            achievement.get("solution", ""),
            " ".join(achievement.get("business_impact", [])),
            " ".join(achievement.get("keywords", [])),
            " ".join(achievement.get("tools", [])),
            " ".join(achievement.get("supports_roles", [])),
            " ".join(achievement.get("secondary_evidence_types", [])),
            achievement.get("category", ""),
            achievement.get("strategic_category", ""),
            achievement.get("evidence_type", ""),
            achievement.get("evidence_maturity", ""),
            " ".join(achievement.get("success_metrics", {}).values())
        ])
    )


def score_achievement(achievement: dict, parsed_job: dict) -> dict:
    job_keywords = [normalize(k) for k in parsed_job.get("keywords", [])]
    job_themes = [normalize(t) for t in parsed_job.get("themes", [])]
    role_type = parsed_job.get("role_type", "")

    ach_keywords = [normalize(k) for k in achievement.get("keywords", [])]
    ach_category = normalize(achievement.get("category", ""))
    ach_roles = [normalize(r) for r in achievement.get("supports_roles", [])]
    ach_text = build_achievement_text(achievement)

    score = 0
    matched_keywords = []

    # 1. Keyword match
    for keyword in job_keywords:
        if keyword in ach_keywords or keyword in ach_text:
            score += 10
            matched_keywords.append(keyword)
        else:
            similarity = max(
                [fuzz.partial_ratio(keyword, ak) for ak in ach_keywords],
                default=0
            )
            if similarity >= 85:
                score += 6
                matched_keywords.append(keyword)

    # 2. Theme match
    for theme in job_themes:
        if theme in ach_category or theme in ach_text:
            score += 8

    # 3. Role support match
    for supported_role in ach_roles:
        if supported_role in ROLE_MAP.get(role_type, []):
            score += 12

    # 4. Company weighting by role type
    company = achievement.get("company", "")
    score += ROLE_COMPANY_WEIGHTS.get(role_type, {}).get(company, 0)


    # 6. Penalize weak/no-match achievements
    if not matched_keywords and score < 25:
        score -= 10

    result = achievement.copy()
    result["match_score"] = score
    result["matched_keywords"] = sorted(set(matched_keywords))

    return result


def deduplicate_achievements(achievements: list) -> list:
    seen_ids = set()
    seen_titles = set()
    unique = []

    for achievement in achievements:
        achievement_id = achievement.get("id")
        title = normalize(achievement.get("title", ""))

        if achievement_id in seen_ids:
            continue

        if title in seen_titles:
            continue

        seen_ids.add(achievement_id)
        seen_titles.add(title)
        unique.append(achievement)

    return unique


def match_achievements(job_text: str, top_n: int = 10) -> dict:
    parsed_job = parse_job_description(job_text)
    achievements = load_json("achievements.json")

    scored = [
        score_achievement(achievement, parsed_job)
        for achievement in achievements
    ]

    ranked = sorted(scored, key=lambda x: x["match_score"], reverse=True)
    ranked = deduplicate_achievements(ranked)

    return {
        "parsed_job": parsed_job,
        "top_achievements": ranked[:top_n],
        "all_ranked_achievements": ranked
    }


if __name__ == "__main__":
    sample_job = """
    Senior Product Manager responsible for APIs, analytics,
    SQL reporting, forecasting, Agile delivery, customer discovery,
    IoT, hardware, software, roadmap, user stories,
    acceptance criteria, and platform integrations.
    """

    results = match_achievements(sample_job, top_n=12)

    print("\nPARSED JOB")
    print(results["parsed_job"])

    print("\nTOP ACHIEVEMENTS")
    for achievement in results["top_achievements"]:
        print(
            achievement["match_score"],
            achievement["id"],
            achievement["company"],
            "-",
            achievement["title"],
            "| matched:",
            achievement.get("matched_keywords", [])
        )