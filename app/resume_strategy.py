# agents/resume_strategy.py

RESUME_COMPOSITION = {
    "technical_pm": {
        "technical_systems": 0.30,
        "product_execution": 0.25,
        "analytics": 0.20,
        "leadership": 0.15,
        "operations": 0.10,
    },
    "data_pm": {
        "analytics": 0.35,
        "technical_systems": 0.25,
        "product_execution": 0.20,
        "leadership": 0.10,
        "operations": 0.10,
    },
    "ai_pm": {
        "technical_systems": 0.25,
        "automation": 0.25,
        "analytics": 0.20,
        "product_execution": 0.20,
        "leadership": 0.10,
    },
    "operations_pm": {
        "operations": 0.35,
        "analytics": 0.20,
        "leadership": 0.20,
        "technical_systems": 0.15,
        "product_execution": 0.10,
    },
    "industrial_pm": {
        "industrial": 0.35,
        "operations": 0.25,
        "technical_systems": 0.20,
        "leadership": 0.10,
        "analytics": 0.10,
    },
    "growth_pm": {
        "growth": 0.35,
        "analytics": 0.25,
        "experimentation": 0.20,
        "automation": 0.10,
        "leadership": 0.10,
    },
}

HARD_DOMAIN_REQUIREMENTS = {
    "retail_pricing_science": {
        "signals": [
            "price elasticity",
            "trade promotion",
            "trade funds",
            "markdown",
            "markdowns",
            "cannibalization",
            "halo effects",
            "category management",
            "category managers",
            "pricing science",
            "promotional roi",
            "retailer-cpg",
            "cpg",
            "retail buyers",
            "trade fund governance",
            "promotion optimization",
            "base pricing",
        ],
        "candidate_evidence": [
            "pricing",
            "forecasting",
            "demand planning",
            "analytics",
        ],
        "gap_label": "Retail pricing science / trade promotion management",
    },
    "enterprise_ai_platform": {
        "signals": [
            "agentic systems",
            "autonomous agents",
            "llm-powered",
            "recommendation engines",
            "ai-native decisioning",
            "real-time data pipelines",
            "ml-powered forecasting",
            "optimization capabilities",
        ],
        "candidate_evidence": [
            "openai",
            "ai agents",
            "automation",
            "python",
            "analytics workflows",
        ],
        "gap_label": "Enterprise-scale AI/ML platform ownership",
    },
}


CREDIBILITY_RULES = {
    "restricted_phrases": [
        "AI-native Product Manager",
        "agentic AI leader",
        "visionary AI Product Manager",
        "AI platform leader",
        "enterprise AI platform PM",
    ],
    "safe_ai_positioning": (
        "Product Manager with hands-on experience building AI-enabled workflows, "
        "automation tools, and analytics systems."
    ),
}
ROLE_STRATEGY = {
    "ai_pm": {
        "headline": "AI Product Manager",
        "positioning": (
            "Hands-on Product Manager who builds AI workflows, automation tools, "
            "and analytics systems that improve operational decision-making."
        ),
        "resume_angle": "AI-native product builder with real operating experience",
        "experience_order": ["LITET", "EMERSON", "CHAMBERLAIN", "LUGO_HERMANOS", "REGAL_REXNORD"],
        "deprioritize": ["REGAL_REXNORD"],
        "skills": [
            "AI Product Strategy",
            "OpenAI APIs",
            "Workflow Automation",
            "Prompt Strategy",
            "Experimentation",
            "Python",
            "Streamlit",
            "Hugging Face",
            "SQL",
            "KPI Systems",
            "Agile",
            "Cross-functional Leadership",
        ],
        "must_highlight": [
            "AI agents",
            "automation",
            "OpenAI APIs",
            "analytics workflows",
            "operational decision support",
            "experimentation",
        ],
        "avoid_overemphasis": [
            "legacy sales",
            "branch operations",
            "industrial distribution unless relevant",
        ],
    },

    "growth_pm": {
        "headline": "E-commerce Growth Manager",
        "positioning": (
            "Growth-focused product operator using analytics, PPC optimization, "
            "pricing, and marketplace strategy to scale revenue."
        ),
        "resume_angle": "e-commerce operator combining growth strategy with analytics",
        "experience_order": ["LITET", "CHAMBERLAIN", "EMERSON", "LUGO_HERMANOS", "REGAL_REXNORD"],
        "deprioritize": ["REGAL_REXNORD"],
        "skills": [
            "E-commerce Growth",
            "Amazon Marketplace",
            "Shopify",
            "PPC Optimization",
            "ROAS Improvement",
            "Pricing Strategy",
            "Inventory Planning",
            "Google Analytics",
            "Python",
            "Power BI",
            "Experimentation",
        ],
        "must_highlight": [
            "Amazon",
            "Shopify",
            "PPC",
            "ROAS",
            "pricing",
            "product listings",
            "inventory planning",
        ],
        "avoid_overemphasis": [
            "enterprise APIs",
            "industrial sales",
            "older branch management",
        ],
    },

    "data_pm": {
        "headline": "Analytics Product Manager",
        "positioning": (
            "Product and analytics leader building KPI systems, dashboards, "
            "forecasting workflows, and decision-support tools."
        ),
        "resume_angle": "data-driven PM who turns fragmented data into scalable analytics products",
        "experience_order": ["LITET", "EMERSON", "CHAMBERLAIN", "LUGO_HERMANOS", "REGAL_REXNORD"],
        "deprioritize": ["REGAL_REXNORD"],
        "skills": [
            "Analytics Strategy",
            "KPI Dashboards",
            "SQL",
            "Python",
            "Power BI",
            "Forecasting",
            "Data Products",
            "Automation",
            "APIs",
            "Roadmap Strategy",
            "Stakeholder Management",
        ],
        "must_highlight": [
            "analytics platforms",
            "dashboards",
            "KPI systems",
            "forecasting",
            "SQL",
            "Python",
            "data products",
        ],
        "avoid_overemphasis": [
            "sales territory management",
            "general operations without analytics connection",
        ],
    },

    "technical_pm": {
        "headline": "Technical Product Manager",
        "positioning": (
            "Technical Product Manager with experience owning API, analytics, "
            "automation, and IoT platform roadmaps."
        ),
        "resume_angle": "technical PM with platform, API, analytics, and cross-functional delivery experience",
        "experience_order": ["EMERSON", "CHAMBERLAIN", "LITET", "LUGO_HERMANOS", "REGAL_REXNORD"],
        "deprioritize": ["REGAL_REXNORD"],
        "skills": [
            "Platform Product Management",
            "APIs",
            "Roadmap Ownership",
            "Agile",
            "RICE Prioritization",
            "IoT",
            "Analytics Platforms",
            "SQL",
            "Python",
            "Cross-functional Leadership",
            "Stakeholder Management",
        ],
        "must_highlight": [
            "APIs",
            "roadmap ownership",
            "Agile delivery",
            "IoT",
            "analytics platforms",
            "technical stakeholders",
        ],
        "avoid_overemphasis": [
            "pure e-commerce growth",
            "legacy sales",
        ],
    },

    "operations_pm": {
        "headline": "Operations Product Manager",
        "positioning": (
            "Product and operations leader with experience building systems for "
            "inventory visibility, forecasting, fulfillment, and process automation."
        ),
        "resume_angle": "systems-oriented PM improving operational execution through analytics and automation",
        "experience_order": ["LITET", "LUGO_HERMANOS", "EMERSON", "CHAMBERLAIN", "REGAL_REXNORD"],
        "deprioritize": ["REGAL_REXNORD"],
        "skills": [
            "Operations Strategy",
            "Inventory Planning",
            "Forecasting",
            "Process Automation",
            "Python",
            "SQL",
            "Power BI",
            "Vendor Management",
            "Workflow Design",
            "KPI Tracking",
        ],
        "must_highlight": [
            "inventory",
            "forecasting",
            "fulfillment",
            "automation",
            "process improvement",
            "vendor coordination",
        ],
        "avoid_overemphasis": [
            "pure software platform work unless tied to operations",
        ],
    },

    "industrial_pm": {
        "headline": "Industrial Product Manager",
        "positioning": (
            "Product Manager with experience in industrial automation, technical sales, "
            "vendor partnerships, inventory planning, and analytics-driven growth."
        ),
        "resume_angle": "industrial PM with technical product, vendor, and commercial ownership",
        "experience_order": ["LUGO_HERMANOS", "EMERSON", "REGAL_REXNORD", "CHAMBERLAIN", "LITET"],
        "deprioritize": [],
        "skills": [
            "Industrial Automation",
            "Technical Product Management",
            "Vendor Negotiations",
            "Inventory Planning",
            "Forecasting",
            "B2B Sales",
            "Product Strategy",
            "Power BI",
            "SQL",
            "Customer Training",
        ],
        "must_highlight": [
            "industrial automation",
            "THK",
            "technical support",
            "vendor negotiations",
            "inventory planning",
            "B2B customers",
        ],
        "avoid_overemphasis": [
            "consumer e-commerce unless showing analytics capability",
        ],
    },
}


def get_composition(role_type: str) -> dict:
    return RESUME_COMPOSITION.get(role_type, RESUME_COMPOSITION["technical_pm"])


def calculate_category_quotas(role_type: str, total_bullets: int) -> dict:
    composition = get_composition(role_type)

    raw_quotas = {
        category: weight * total_bullets
        for category, weight in composition.items()
    }

    quotas = {
        category: max(1, round(value))
        for category, value in raw_quotas.items()
    }

    difference = total_bullets - sum(quotas.values())

    if difference != 0:
        sorted_categories = sorted(
            raw_quotas,
            key=raw_quotas.get,
            reverse=True
        )

        index = 0
        while difference != 0:
            category = sorted_categories[index % len(sorted_categories)]

            if difference > 0:
                quotas[category] += 1
                difference -= 1

            elif difference < 0 and quotas[category] > 1:
                quotas[category] -= 1
                difference += 1

            index += 1

    return quotas

def detect_hard_domain_gaps(job_description: str | None) -> list[dict]:
    if not job_description:
        return []

    text = job_description.lower()
    gaps = []

    for domain, config in HARD_DOMAIN_REQUIREMENTS.items():
        matched_signals = [
            signal for signal in config["signals"]
            if signal in text
        ]

        if matched_signals:
            gaps.append({
                "domain": domain,
                "gap_label": config["gap_label"],
                "matched_signals": matched_signals,
                "severity": "high" if len(matched_signals) >= 4 else "medium",
            })

    return gaps


def adjust_positioning_for_credibility(
    role_type: str,
    role_strategy: dict,
    hard_domain_gaps: list[dict]
) -> tuple[str, str]:
    positioning = role_strategy["positioning"]
    resume_angle = role_strategy["resume_angle"]

    if role_type == "ai_pm":
        positioning = (
            "Product Manager with hands-on experience building AI-enabled workflows, "
            "automation tools, and analytics systems that improve operational decision-making."
        )
        resume_angle = "hands-on automation and analytics PM with applied AI workflow experience"

    if hard_domain_gaps:
        positioning = (
            "Technical Product Manager with experience building analytics, automation, "
            "API, and operational systems across IoT, e-commerce, and industrial environments."
        )
        resume_angle = (
            "credible technical PM with transferable analytics, automation, and platform experience; "
            "position around adjacent strengths while acknowledging domain-specific gaps"
        )

    return positioning, resume_angle

def build_resume_strategy(
    role_type: str,
    total_bullets: int = 12,
    fit_evaluation: dict | None = None,
    job_description: str | None = None,
) -> dict:
    role_type = (role_type or "technical_pm").lower()

    composition = get_composition(role_type)
    category_quotas = calculate_category_quotas(role_type, total_bullets)

    role_strategy = ROLE_STRATEGY.get(
        role_type,
        ROLE_STRATEGY["technical_pm"]
    )

    hard_domain_gaps = detect_hard_domain_gaps(job_description)

    positioning, resume_angle = adjust_positioning_for_credibility(
        role_type=role_type,
        role_strategy=role_strategy,
        hard_domain_gaps=hard_domain_gaps
    )

    strategy = {
        "role_type": role_type,
        "headline": role_strategy["headline"],
        "positioning": positioning,
        "resume_angle": resume_angle,
        "hard_domain_gaps": hard_domain_gaps,
        "credibility_rules": CREDIBILITY_RULES,
        "experience_order": role_strategy["experience_order"],
        "deprioritize": role_strategy["deprioritize"],
        "skills": role_strategy["skills"],
        "must_highlight": role_strategy["must_highlight"],
        "avoid_overemphasis": role_strategy["avoid_overemphasis"],
        "composition": composition,
        "category_quotas": category_quotas,
        "total_bullets": total_bullets,
        "generation_rules": [
            "Use the bullet library as source material, not final copy.",
            "Rewrite bullets to match the specific job description.",
            "Follow category quotas, but prioritize relevance over exact math.",
            "Do not treat every past role equally.",
            "Use the experience order unless the job description strongly suggests otherwise.",
            "Deprioritize older or less relevant roles.",
            "Make the summary and skills section clearly different by role type.",
            "Avoid repeating the same sentence structure across bullets.",
            "Do not over-position Ricardo as an AI-native platform PM unless the evidence directly supports enterprise AI product ownership.",
            "If hard_domain_gaps are present, use adjacent positioning instead of claiming direct domain expertise.",
            "Do not claim expertise in pricing science, trade promotion, retail economics, CPG workflows, or category management unless directly supported by achievement evidence.",
            "Prefer credible transferable positioning over inflated alignment.",
        ],
    }

    if fit_evaluation:
        strategy["fit_evaluation"] = fit_evaluation

    if job_description:
        strategy["job_description"] = job_description

    return strategy