import re
from collections import Counter
from app.narrative_modes import NARRATIVE_MODES


ROLE_KEYWORDS = {
    "technical_pm": [
        "api", "apis", "technical", "integration", "platform",
        "backend", "infrastructure", "iot", "systems", "architecture",
        "hardware", "software", "firmware", "acceptance criteria",
        "user stories"
    ],

    "data_pm": [
        "analytics", "sql", "kpi", "kpis", "dashboard",
        "forecasting", "data pipelines", "business intelligence",
        "metrics", "reporting", "quantitative data"
    ],

    "ai_pm": [
        "ai", "llm", "llms", "openai", "anthropic", "llama",
        "machine learning", "artificial intelligence", "ai-driven",
        "ai powered", "ai-powered", "agent", "agents", "agentic",
        "ai agents", "ai agent", "reasoning", "reason and take action",
        "prompt", "prompting", "automation", "automate",
        "workflow automation", "ai workflows", "ai workflow",
        "voice models", "cartesia", "eleven labs"
    ],

    "operations_pm": [
        "inventory", "supply chain", "operations",
        "forecasting", "warehouse", "warehousing", "logistics",
        "freight", "shipping", "fulfillment", "replenishment",
        "process workflows", "standard operating procedures",
        "implementation plans", "deployment"
    ],

    "industrial_pm": [
        "manufacturing", "industrial", "oem",
        "maintenance", "reliability", "automation systems",
        "assets", "mixed assets", "hardware", "physical layer",
        "physical-world"
    ],

    "growth_pm": [
        "growth", "conversion", "marketplace", "ecommerce",
        "e-commerce", "ppc", "roas", "acquisition",
        "retention", "go-to-market", "adoption", "pricing",
        "self-serve", "self serve", "self-onboarding", "self onboarding"
    ]
}


ROLE_WEIGHTS = {
    "technical_pm": 1.0,
    "data_pm": 1.0,
    "ai_pm": 2.2,
    "operations_pm": 1.2,
    "industrial_pm": 1.1,
    "growth_pm": 1.0,
}


HIGH_SIGNAL_PHRASES = {
    "ai_pm": [
        "ai agents",
        "ai agent",
        "ai-driven agents",
        "agentic applications",
        "ai that can reason",
        "reason and take action",
        "using ai",
        "llm",
        "llms",
        "openai",
        "anthropic",
        "machine learning",
        "artificial intelligence",
    ],
    "operations_pm": [
        "logistics",
        "freight brokerage",
        "shipping",
        "warehouse technologies",
        "fulfillment industry",
        "physical layer",
        "complex industries with a physical layer",
    ],
    "growth_pm": [
        "go-to-market",
        "pricing",
        "self-onboarding",
        "self-serve help",
    ],
}


COMMON_KEYWORDS = [
    "python", "sql", "apis", "api", "rest api", "analytics",
    "forecasting", "automation", "ai", "llm", "llms", "openai",
    "anthropic", "machine learning", "artificial intelligence",
    "agent", "agents", "agentic", "power bi", "databricks",
    "snowflake", "azure", "aws", "etl", "dashboard", "reporting",
    "data pipelines", "quantitative data",

    "agile", "scrum", "roadmap", "product vision",
    "release plans", "product lifecycle", "feature lifecycle",
    "user stories", "acceptance criteria", "epics",
    "backlog", "prioritization", "mvp", "experimentation",
    "product strategy", "go-to-market", "pricing",

    "customer discovery", "voice of customer", "end-user research",
    "customer value", "user adoption", "user utility",
    "personas", "wireframes", "process workflows",
    "acceptance testing", "uat", "quality assurance", "qa",
    "onsite", "shadow users", "user feedback",

    "stakeholder management", "cross-functional", "design",
    "engineering", "software", "hardware", "firmware",
    "customer success", "marketing", "data science",

    "iot", "connected devices", "telemetry", "asset tracking",
    "mixed assets", "inventory", "supply chain", "operations",
    "warehouse", "warehousing", "logistics", "freight",
    "shipping", "fulfillment", "maintenance", "reliability",
    "industrial", "manufacturing", "physical layer"
]


SEMANTIC_EXPANSIONS = {
    "ai": [
        "llm", "ai agents", "agentic applications", "automation",
        "prompt strategy", "ai workflows", "reasoning"
    ],

    "llm": [
        "openai", "anthropic", "ai agents", "prompt strategy",
        "agentic applications"
    ],

    "agentic": [
        "ai agents", "reasoning", "automation", "ai workflows"
    ],

    "logistics": [
        "shipping", "freight", "warehouse", "fulfillment",
        "supply chain", "operations", "physical layer"
    ],

    "iot": [
        "connected devices", "telemetry", "hardware", "firmware",
        "asset tracking", "platform", "field operations"
    ],

    "mixed assets": [
        "asset tracking", "field operations", "hardware",
        "iot", "industrial assets", "operations"
    ],

    "hardware": [
        "firmware", "connected devices", "iot",
        "physical systems", "cross-functional engineering"
    ],

    "analytics": [
        "kpis", "dashboards", "reporting", "forecasting",
        "data-driven", "quantitative analysis"
    ],

    "roadmap": [
        "product vision", "release plans",
        "feature prioritization", "stakeholder alignment"
    ],

    "product lifecycle": [
        "planning", "development", "launch", "deployment",
        "maintenance", "feature lifecycle"
    ],

    "user stories": [
        "acceptance criteria", "epics", "backlog", "agile delivery"
    ],

    "acceptance criteria": [
        "user stories", "uat", "quality assurance", "qa"
    ],

    "customer discovery": [
        "voice of customer", "end-user research",
        "customer interviews", "customer pain points"
    ],

    "voice of customer": [
        "customer discovery", "end-user research",
        "customer interviews", "customer pain points"
    ],

    "operations": [
        "inventory", "supply chain", "maintenance",
        "warehouse", "field operations", "process improvement"
    ],

    "industrial": [
        "manufacturing", "mechanical", "motion systems",
        "reliability", "industrial assets", "field operations"
    ],

    "automation": [
        "process improvement", "efficiency",
        "workflow automation", "operational automation",
        "ai workflows"
    ],

    "go-to-market": [
        "marketing", "customer success", "launch", "adoption",
        "pricing"
    ]
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def count_keyword_occurrences(text: str, keyword: str) -> int:
    pattern = r"\b" + re.escape(keyword) + r"\b"
    return len(re.findall(pattern, text))


def score_role_types(text: str) -> dict:
    scores = Counter()

    for role, keywords in ROLE_KEYWORDS.items():
        for keyword in keywords:
            count = count_keyword_occurrences(text, keyword)

            if count:
                scores[role] += count * ROLE_WEIGHTS.get(role, 1.0)

    for role, phrases in HIGH_SIGNAL_PHRASES.items():
        for phrase in phrases:
            if phrase in text:
                scores[role] += 3

    return dict(scores)


def detect_role_type(text: str) -> str:
    scores = score_role_types(text)

    if not scores:
        return "technical_pm"

    # Override: AI-native jobs should not get buried under technical/platform words.
    ai_score = scores.get("ai_pm", 0)
    technical_score = scores.get("technical_pm", 0)
    operations_score = scores.get("operations_pm", 0)

    if ai_score >= 6 and ai_score >= technical_score * 0.65:
        return "ai_pm"

    if ai_score >= 6 and operations_score >= 4:
        return "ai_pm"

    return max(scores, key=scores.get)

def normalize_role_type(role_type: str, text: str) -> str:

    operational_signals = [
        "forecasting",
        "planning",
        "inventory",
        "replenishment",
        "operations",
        "operational",
        "fulfillment",
        "logistics",
        "warehouse",
        "supply chain",
        "telemetry",
        "incident",
        "sla",
        "alerting",
        "workflow",
        "execution",
        "reliability",
        "optimization",
        "scheduling",
        "capacity",
        "demand",
        "adoption",
        "rollout",
        "scalability",
        "decisioning",
    ]

    platform_signals = [
        "roadmap",
        "cross-functional",
        "enterprise",
        "platform",
        "multi-quarter",
        "delivery",
        "customer impact",
        "business outcomes",
    ]

    ai_signals = [
        "llm",
        "agentic",
        "openai",
        "ai-native",
        "generative ai",
        "autonomous",
        "machine learning",
    ]

    ops_count = sum(1 for s in operational_signals if s in text)
    platform_count = sum(1 for s in platform_signals if s in text)
    ai_count = sum(1 for s in ai_signals if s in text)

    # AI + operational systems -> operations PM
    if role_type == "ai_pm" and ops_count >= 4:
        return "operations_pm"

    # Enterprise operational platform
    if ops_count >= 5 and platform_count >= 2:
        return "operations_pm"

    # Pure AI/software platform
    if ai_count >= 3 and ops_count <= 2:
        return "ai_pm"

    return role_type

def extract_keywords(text: str) -> list:
    found = []

    for keyword in COMMON_KEYWORDS:
        if keyword in text:
            found.append(keyword)

    return sorted(set(found))


def expand_keywords(found_keywords: list) -> list:
    expanded = set(found_keywords)

    for keyword in found_keywords:
        keyword_lower = keyword.lower()

        if keyword_lower in SEMANTIC_EXPANSIONS:
            expanded.update(SEMANTIC_EXPANSIONS[keyword_lower])

    return sorted(expanded)


def detect_seniority(text: str) -> str:
    seniority_levels = {
        "director": ["director", "head of", "vp"],
        "senior": ["senior", "sr.", "principal", "lead", "leads", "6 years", "6+"],
        "mid": ["product manager", "manager"],
        "junior": ["associate", "junior", "entry level"]
    }

    for level, keywords in seniority_levels.items():
        for keyword in keywords:
            if keyword in text:
                return level

    return "unknown"


def extract_themes(text: str, expanded_keywords: list | None = None) -> list:
    themes = []

    keyword_text = " ".join(expanded_keywords or [])
    combined_text = f"{text} {keyword_text}"

    theme_map = {
        "AI / Automation": [
            "ai", "automation", "llm", "llms", "openai",
            "anthropic", "agent", "agents", "agentic",
            "ai agents", "workflow automation", "process improvement",
            "reasoning"
        ],

        "Analytics": [
            "analytics", "kpi", "kpis", "dashboard",
            "metrics", "reporting", "quantitative data",
            "data-driven"
        ],

        "APIs / Platform": [
            "api", "apis", "platform", "integration",
            "rest api", "enterprise integrations"
        ],

        "IoT / Connected Devices": [
            "iot", "connected devices", "telemetry",
            "hardware", "firmware", "asset tracking"
        ],

        "Operations / Assets": [
            "inventory", "supply chain", "warehouse",
            "warehousing", "logistics", "freight", "shipping",
            "fulfillment", "mixed assets", "field operations",
            "maintenance", "physical layer"
        ],

        "Industrial": [
            "manufacturing", "industrial", "oem",
            "maintenance", "reliability", "industrial assets"
        ],

        "Agile Product Delivery": [
            "agile", "scrum", "backlog", "jira",
            "sprint", "user stories", "acceptance criteria",
            "epics", "uat", "qa"
        ],

        "Customer Discovery": [
            "customer discovery", "voice of customer",
            "customer interviews", "user research",
            "end-user research", "customer pain points",
            "onsite", "shadow users", "user feedback"
        ],

        "Go-To-Market": [
            "go-to-market", "marketing", "customer success",
            "adoption", "launch", "pricing", "self-serve",
            "self-onboarding"
        ]
    }

    for theme, keywords in theme_map.items():
        if any(keyword in combined_text for keyword in keywords):
            themes.append(theme)

    return themes


def parse_job_description(job_text: str) -> dict:
    clean = clean_text(job_text)

    base_keywords = extract_keywords(clean)
    expanded_keywords = expand_keywords(base_keywords)
    

    return {
        "role_type": normalize_role_type(detect_role_type(clean), clean),
        "role_scores": score_role_types(clean),
        "seniority": detect_seniority(clean),
        "keywords": expanded_keywords,
        "base_keywords": base_keywords,
        "semantic_keywords": sorted(set(expanded_keywords) - set(base_keywords)),
        "themes": extract_themes(clean, expanded_keywords),
        "narrative_mode": detect_narrative_mode(clean),
        "clean_text": clean,
        "raw_text": job_text
    }

def detect_narrative_mode(text: str) -> str:
    scores = {}

    for mode, config in NARRATIVE_MODES.items():
        score = 0

        for signal in config["signals"]:
            if signal in text:
                score += 1

        scores[mode] = score

    best_mode = max(scores, key=scores.get)

    if scores[best_mode] == 0:
        return "ENTERPRISE_PLATFORM"

    return best_mode