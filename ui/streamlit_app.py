import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import pandas as pd
import streamlit as st

from app.job_parser import parse_job_description
from app.matcher import match_achievements
from app.resume_generator import generate_resume_outline
from app.ats_optimizer import analyze_keyword_coverage
from app.export_pdf import save_resume_pdf
from app.fit_analyzer import analyze_role_fit
from app.application_answer_generator import generate_application_answer
from app.cover_letter_generator import generate_cover_letter
from app.company_extractor import extract_company_name
from app.export_cover_letter_pdf import save_cover_letter_pdf
from app.resume_strategy_agent import build_resume_strategy_from_jd


st.set_page_config(
    page_title="Resume Agent",
    layout="wide"
)

st.title("Resume Agent")
st.caption("AI-powered resume positioning engine for Product Manager roles.")

job_text = st.text_area(
    "Job Description",
    height=350,
    placeholder="Paste job listing here...",
    key="job_text"
)

top_n = 12

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


if st.button("Analyze Job", key="analyze_job_button"):

    if not job_text.strip():
        st.warning("Please paste a job description.")
        st.stop()

    with st.spinner("Analyzing role, matching achievements, and generating resume strategy..."):

        parsed = parse_job_description(job_text)

        matches = match_achievements(
            job_text,
            top_n=200
        )

        resume_strategy = build_resume_strategy_from_jd(
            job_description=job_text,
            selected_achievements=matches["top_achievements"]
        )

        outline = generate_resume_outline(
            job_text,
            top_n=top_n,
            resume_strategy=resume_strategy,
            match_results=matches
        )

        ats = analyze_keyword_coverage(
            job_text,
            top_n=top_n
        )

        fit_analysis = analyze_role_fit(
            parsed,
            outline["selected_achievements"]
        )

    st.session_state.analysis_done = True
    st.session_state.parsed = parsed
    st.session_state.matches = matches
    st.session_state.outline = outline
    st.session_state.ats = ats
    st.session_state.fit_analysis = fit_analysis
    st.session_state.resume_strategy = resume_strategy


if st.session_state.analysis_done:

    parsed = st.session_state.parsed
    matches = st.session_state.matches
    outline = st.session_state.outline
    ats = st.session_state.ats
    fit_analysis = st.session_state.fit_analysis
    resume_strategy = st.session_state.resume_strategy

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Fit Analysis",
        "Strategy",
        "Resume Preview",
        "Matched Achievements",
        "ATS Analysis",
        "Application Questions",
        "Cover Letter"
    ])

    with tab1:
        st.subheader("Role Fit Evaluation")

        st.metric("Fit Score", f'{fit_analysis["fit_score"]}/10')
        st.metric("Fit Level", fit_analysis["fit_level"])
        st.metric("Worth Applying", "Yes" if fit_analysis["worth_applying"] else "No")

        st.divider()

        st.subheader("Dimension Scores")
        st.json(fit_analysis["dimension_scores"])

        st.subheader("Strengths")
        for item in fit_analysis["strengths"]:
            st.write(f"• {item}")

        st.subheader("Main Gaps")
        for item in fit_analysis["gaps"]:
            st.write(f"• {item}")

        st.subheader("Positioning Advice")
        st.write(fit_analysis["positioning_advice"])

    with tab2:
        st.subheader("Resume Strategy")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Target Positioning",
                resume_strategy.get("target_positioning", parsed.get("role_type", ""))
            )
            st.metric("Seniority", parsed.get("seniority", ""))

        with col2:
            st.write("Resume Narrative:")
            st.write(resume_strategy.get("resume_narrative", ""))

            st.write("Fit Level:")
            st.write(resume_strategy.get("fit_level", ""))

        st.divider()

        st.subheader("Winning Story")
        st.write(resume_strategy.get("winning_story", ""))

        st.subheader("Primary Angle")
        st.write(resume_strategy.get("primary_angle", ""))

        st.subheader("Secondary Angle")
        st.write(resume_strategy.get("secondary_angle", ""))

        st.subheader("Avoid Angle")
        st.write(resume_strategy.get("avoid_angle", ""))

        st.subheader("Why Hire This Person")
        st.write(resume_strategy.get("why_hire_this_person", ""))

        st.subheader("Recruiter Pitch")
        st.write(resume_strategy.get("recruiter_pitch", ""))
        
        st.subheader("Role Dimensions")
        st.json(resume_strategy.get("role_dimensions", []))

        st.subheader("Selection Priorities")
        st.write(resume_strategy.get("selection_priorities", []))

        st.subheader("Primary Strengths")
        st.write(resume_strategy.get("primary_strengths", []))

        st.subheader("Credible Adjacencies")
        st.write(resume_strategy.get("credible_adjacencies", []))

        st.subheader("Hard Gaps")
        st.write(resume_strategy.get("hard_gaps", []))

        st.subheader("Positioning Advice")
        st.write(resume_strategy.get("positioning_advice", ""))

    with tab3:
        st.subheader("Professional Summary")

        edited_summary = st.text_area(
            "Summary",
            value=outline["summary"],
            height=120,
            key="edited_summary"
        )

        st.divider()

        st.subheader("Resume Bullet Outline")

        for company, bullets in outline["bullets_by_company"].items():
            st.markdown(f"### {company}")
            for bullet in bullets:
                st.write(bullet)

        st.divider()
        st.subheader("Export Resume")

        if st.button("Generate Resume PDF", key="resume_pdf_export_button"):

            with st.spinner("Generating PDF..."):
                outline_for_pdf = {
                    **st.session_state.outline,
                    "summary": st.session_state.edited_summary
                }

                output_path = save_resume_pdf(
                    job_text=st.session_state.job_text,
                    top_n=top_n,
                    resume_strategy=resume_strategy,
                    outline_override=outline_for_pdf
                )

            st.session_state.outline = outline_for_pdf
            st.session_state.pdf_path = output_path
            st.success(f"PDF generated: {output_path}")

        if "pdf_path" in st.session_state:
            with open(st.session_state.pdf_path, "rb") as f:
                st.download_button(
                    label="Download Resume PDF",
                    data=f,
                    file_name=Path(st.session_state.pdf_path).name,
                    mime="application/pdf",
                    key="download_resume_pdf_button"
                )

    with tab4:
        st.subheader("Top Matched Achievements")

        for ach in matches["top_achievements"]:
            with st.expander(
                f'{ach.get("match_score")} | {ach.get("company")} | {ach.get("title")}'
            ):
                st.write("Category:", ach.get("category"))
                st.write("Strategic Category:", ach.get("strategic_category"))
                st.write("Description:", ach.get("description"))
                st.write("Business Problem:", ach.get("business_problem"))
                st.write("Solution:", ach.get("solution"))
                st.write("Business Impact:", ach.get("business_impact"))
                st.write("Metrics:", ach.get("metrics"))
                st.write("Matched Keywords:", ach.get("matched_keywords"))

    with tab5:
        st.subheader("ATS Keyword Coverage")

        col1, col2, col3 = st.columns(3)

        col1.metric("Coverage Rate", ats["coverage_rate"])
        col2.metric("Covered Keywords", len(ats["covered_keywords"]))
        col3.metric("Missing Keywords", len(ats["missing_keywords"]))

        st.divider()

        st.write("Covered Keywords")
        st.write(ats["covered_keywords"])

        st.write("Missing Keywords")
        st.write(ats["missing_keywords"])

    with tab6:
        st.subheader("Application Question Answer Generator")

        company_name = st.text_input(
            "Company Name",
            placeholder="RevenueCat, Higharc, RevStar...",
            key="app_answer_company_name"
        )

        app_question = st.text_area(
            "Application Question",
            height=120,
            placeholder="Paste the application question here...",
            key="app_question_text"
        )

        answer_length = st.selectbox(
            "Answer Length",
            ["short", "medium", "long"],
            index=1,
            key="app_answer_length"
        )

        if st.button("Generate Answer", key="generate_application_answer_button"):
            if not app_question.strip():
                st.warning("Please paste an application question.")
                st.stop()

            with st.spinner("Generating tailored answer..."):
                answer = generate_application_answer(
                    question=app_question,
                    job_text=st.session_state.job_text,
                    parsed_job=parsed,
                    selected_achievements=outline["selected_achievements"],
                    company_name=company_name,
                    answer_length=answer_length
                )

            st.text_area(
                "Generated Answer",
                value=answer,
                height=260,
                key="generated_application_answer"
            )

    with tab7:
        st.subheader("Cover Letter Generator")

        detected_company = extract_company_name(st.session_state.job_text)

        company_name = st.text_input(
            "Company Name",
            value=detected_company,
            placeholder="Auto-detected from job post when possible",
            key="cover_letter_company_name"
        )

        hiring_manager = st.text_input(
            "Hiring Manager",
            placeholder="Leave blank if unknown",
            key="cover_letter_hiring_manager_input"
        )

        company_research = st.text_area(
            "Company Research / Notes",
            height=180,
            placeholder="Paste company research, mission, product notes, recent news, or why the company interests you...",
            key="cover_letter_company_research"
        )

        tone = st.selectbox(
            "Tone",
            ["human", "concise", "confident", "warm", "executive"],
            index=0,
            key="cover_letter_tone"
        )

        if st.button("Generate Cover Letter", key="generate_cover_letter_button"):
            with st.spinner("Generating tailored cover letter..."):
                cover_letter = generate_cover_letter(
                    job_text=st.session_state.job_text,
                    parsed_job=parsed,
                    selected_achievements=outline["selected_achievements"],
                    company_name=company_name,
                    company_research=company_research,
                    hiring_manager=hiring_manager,
                    tone=tone
                )

            st.session_state.cover_letter = cover_letter
            st.session_state.cover_letter_company = company_name
            st.session_state.cover_letter_hiring_manager = hiring_manager

        if "cover_letter" in st.session_state:
            st.text_area(
                "Generated Cover Letter",
                value=st.session_state.cover_letter,
                height=420,
                key="generated_cover_letter_text"
            )

            if st.button("Export Cover Letter PDF", key="export_cover_letter_pdf_button"):
                with st.spinner("Generating cover letter PDF..."):
                    output_path = save_cover_letter_pdf(
                        cover_letter=st.session_state.cover_letter,
                        company_name=st.session_state.cover_letter_company,
                        hiring_manager=st.session_state.cover_letter_hiring_manager
                    )

                st.success(f"Cover letter PDF generated: {output_path}")

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="Download Cover Letter PDF",
                        data=f,
                        file_name=Path(output_path).name,
                        mime="application/pdf",
                        key="download_cover_letter_pdf_button"
                    )