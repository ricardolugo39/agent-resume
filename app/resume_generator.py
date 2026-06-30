from app.matcher import match_achievements
from app.bullet_rewriter import rewrite_bullet
from app.summary_generator import generate_summary
from app.resume_strategy import build_resume_strategy
from app.resume_strategy_agent import build_resume_strategy_from_jd
from app.achievement_selector import select_achievements_with_strategy
from app.company_section_generator import generate_company_section
from app.candidate_fit_agent import evaluate_candidate_fit


def achievement_to_bullet(
    achievement: dict,
    parsed_job: dict,
    resume_strategy: dict | None = None,
    use_llm: bool = True
) -> str:
    if use_llm:
        try:
            return rewrite_bullet(
                achievement=achievement,
                parsed_job=parsed_job,
                resume_strategy=resume_strategy
            )
        except Exception as e:
            print(f"LLM rewrite failed for {achievement.get('id')}: {e}")

    description = achievement.get("description", "")
    impact = achievement.get("business_impact", [])

    if impact:
        return f"- {description} {impact[0]}."

    return f"- {description}."


def generate_resume_outline(
    job_text: str,
    top_n: int = 10,
    candidate_fit: dict | None = None,
    resume_strategy: dict | None = None,
    match_results: dict | None = None,
    rewrite_plan: dict | None = None,
) -> dict:

    if match_results is None:
        results = match_achievements(job_text, top_n=200)
    else:
        results = match_results

    parsed_job = results["parsed_job"]

    achievements = results.get(
        "all_ranked_achievements",
        results.get("top_achievements", [])
    )

    achievements_for_strategy = achievements[:50]

    if candidate_fit is None:
        candidate_fit = evaluate_candidate_fit(
            job_text=job_text
        )

    if resume_strategy is None:
        try:
            resume_strategy = build_resume_strategy_from_jd(
                job_description=job_text,
                candidate_fit=candidate_fit,
                selected_achievements=achievements_for_strategy
            )
        except Exception as e:
            print(f"Strategy agent failed: {e}")

            role_type = parsed_job.get("role_type", "technical_pm")
            resume_strategy = build_resume_strategy(
                role_type=role_type,
                total_bullets=top_n,
                job_description=job_text
            )

    selected_achievements = select_achievements_with_strategy(
        achievements=achievements[:80],
        resume_strategy=resume_strategy,
        top_n=top_n
    )

    print("\nSELECTED ACHIEVEMENTS")
    print("=" * 80)

    for ach in selected_achievements:
        print(
            ach.get("id"),
            "|",
            ach.get("company"),
            "|",
            ach.get("evidence_type"),
            "|",
            ach.get("title")
        )

    print("=" * 80)

    MAX_BULLETS_PER_COMPANY = 4

    bullets_by_company = {}
    company_achievements = {}

    for achievement in selected_achievements:
        company = achievement.get("company")

        if not company:
            continue

        company_achievements.setdefault(company, [])
        company_achievements[company].append(achievement)

    for company, achievements_for_company in company_achievements.items():
        bullets_by_company[company] = generate_company_section(
            company=company,
            achievements=achievements_for_company,
            parsed_job=parsed_job,
            resume_strategy=resume_strategy,
            max_bullets=min(
                MAX_BULLETS_PER_COMPANY,
                len(achievements_for_company)
            )
        )

    try:
        summary = generate_summary(
            parsed_job=parsed_job,
            selected_achievements=selected_achievements,
            resume_strategy=resume_strategy
        )
    except Exception as e:
        print(f"LLM summary failed: {e}")

        summary = (
            resume_strategy.get("recruiter_pitch")
            or resume_strategy.get("winning_story")
            or "Product Manager with experience leading platform strategy, roadmap execution, and cross-functional product development."
        )

    return {
        "summary": summary,
        "parsed_job": parsed_job,
        "candidate_fit": candidate_fit,
        "resume_strategy": resume_strategy,
        "bullets_by_company": bullets_by_company,
        "selected_achievements": selected_achievements
    }