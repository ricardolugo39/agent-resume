import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ACH_PATH = BASE_DIR / "data" / "achievements.json"

STRATEGIC_CATEGORY_MAP = {
    "ACH_001": "automation",
    "ACH_002": "experimentation",
    "ACH_003": "operations",
    "ACH_004": "growth",
    "ACH_005": "technical_systems",
    "ACH_006": "analytics",
    "ACH_007": "product_execution",
    "ACH_008": "analytics",
    "ACH_009": "operations",
    "ACH_010": "operations",
    "ACH_011": "analytics",
    "ACH_012": "experimentation",
    "ACH_013": "technical_systems",
    "ACH_014": "product_execution",
    "ACH_015": "product_execution",
    "ACH_016": "leadership",
    "ACH_017": "leadership",
    "ACH_018": "operations",
    "ACH_019": "operations",
    "ACH_020": "industrial",
    "ACH_021": "automation",
    "ACH_022": "operations",
    "ACH_023": "technical_systems",
    "ACH_024": "analytics",
    "ACH_025": "leadership",
    "ACH_026": "technical_systems",
    "ACH_027": "technical_systems",
    "ACH_028": "industrial",
    "ACH_029": "industrial",
    "ACH_030": "industrial",
}


def load_achievements():
    with open(ACH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_achievements(achievements):
    with open(ACH_PATH, "w", encoding="utf-8") as f:
        json.dump(achievements, f, indent=2, ensure_ascii=False)


def clean_and_update():
    achievements = load_achievements()

    cleaned = []
    seen_ids = set()

    for ach in achievements:
        ach_id = ach.get("id")

        if not ach_id:
            continue

        if ach_id in seen_ids:
            print(f"Removing duplicate: {ach_id}")
            continue

        seen_ids.add(ach_id)

        strategic_category = STRATEGIC_CATEGORY_MAP.get(ach_id)

        if strategic_category:
            ach["strategic_category"] = strategic_category
        else:
            print(f"Warning: No strategic category found for {ach_id}")

        cleaned.append(ach)

    save_achievements(cleaned)

    print(f"Updated achievements.json")
    print(f"Total unique achievements: {len(cleaned)}")


if __name__ == "__main__":
    clean_and_update()