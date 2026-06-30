from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


@dataclass
class Candidate:
    name: str
    profile: str
    experiences: list[dict[str, Any]]
    achievements: list[dict[str, Any]]

    @classmethod
    def load(cls, name: str = "ricardo") -> "Candidate":
        if name.lower() != "ricardo":
            raise ValueError(f"Unsupported candidate: {name}")

        return cls(
        name="Ricardo Lugo",
        profile=load_ricardo_profile(),
        experiences=load_json("experiences.json"),
        achievements=load_json("achievements.json"),
    )


def load_json(filename: str) -> Any:
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_ricardo_profile() -> str:
    return """
Ricardo Lugo is a Product Manager and technical product operator with experience across
enterprise software, IoT platforms, analytics products, APIs, e-commerce operations,
industrial automation, and applied AI workflows.

He has worked as a Software Product Manager at Chamberlain Group, Product Manager for
analytics and API platforms at Emerson, founder/operator of LITET, and product/branch
leader in industrial distribution at Lugo Hermanos.

His strongest proven themes include:
- Technical Product Management
- Enterprise analytics products
- API and platform products
- IoT and connected-device ecosystems
- Product analytics and KPI systems
- Cross-functional product delivery
- E-commerce growth and operations
- Inventory, forecasting, and unit economics systems
- Applied AI workflows and RAG-based knowledge systems

He should be positioned based on proven product management and technical product
experience first, with AI and founder/operator experience used as supporting evidence
when relevant.
""".strip()