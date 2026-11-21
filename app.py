import streamlit as st

from analyzer.parser import extract_text_from_bytes, extract_text_from_file
from analyzer.nlp_engine import analyze_resume_vs_jd, calculate_originality
from analyzer.ai_client import generate_ai_critique
from analyzer.templates import PRESET_JOB_DESCRIPTIONS

st.set_page_config(
    page_title="ResumeIQ - AI Resume Checker",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root { --navy:#14213d; --blue:#2563eb; --muted:#64748b; --border:#e2e8f0; }
        .block-container { max-width: 1180px; padding-top: 1.25rem; }
        [data-testid="stSidebar"] { background:#f8fafc; border-right:1px solid #e2e8f0; }
        [data-testid="stHeader"] { background:transparent; }
        h1,h2,h3 { color:var(--navy); letter-spacing:-0.02em; }
        .brand { display:flex; align-items:center; gap:.65rem; margin-bottom:.15rem; }
        .brand-mark { width:38px;height:38px;border-radius:10px;background:#2563eb;color:white;
            display:grid;place-items:center;font-weight:800;font-size:18px; }
        .brand-name { font-size:1.25rem;font-weight:800;color:#14213d; }
        .hero { background:linear-gradient(135deg,#172554 0%,#1e3a8a 55%,#2563eb 100%);
            border-radius:18px;padding:34px 38px;color:white;margin-bottom:20px; }
        .hero h1 { color:white;font-size:2.15rem;margin:0 0 8px 0; }
        .hero p { color:#dbeafe;margin:0;font-size:1rem; }
        .step-label { color:#64748b;font-size:.78rem;font-weight:800;text-transform:uppercase;
            letter-spacing:.08em;margin-bottom:.35rem; }
        .metric-shell { background:white;border:1px solid var(--border);border-radius:14px;
            padding:18px 16px;text-align:center;min-height:128px; }
        .metric-shell .label { color:#64748b;font-size:.78rem;font-weight:800;text-transform:uppercase; }
        .metric-shell .value { color:#14213d;font-size:2rem;font-weight:800;line-height:1.15;margin:8px 0 4px; }
        .metric-shell .detail { color:#64748b;font-size:.82rem; }
        .status-pill { display:inline-block;border-radius:999px;padding:5px 10px;font-size:.78rem;font-weight:700; }
        .status-green { background:#dcfce7;color:#166534; }
        .status-amber { background:#fef3c7;color:#92400e; }
        .status-red { background:#fee2e2;color:#991b1b; }
        .insight-card { background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px;margin-bottom:12px; }
        .rewrite-card { border:1px solid #e2e8f0;border-left:4px solid #2563eb;border-radius:10px;
            padding:16px;margin:10px 0;background:white; }
        .privacy-note { color:#94a3b8;font-size:.78rem;margin-top:12px; }
        div.stButton > button { border-radius:9px;height:44px;font-weight:700; }
        div[data-testid="stTabs"] button { font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">R</div><div class="brand-name">ResumeIQ</div></div>',
        unsafe_allow_html=True,
    )
    st.caption("Professional resume intelligence")
    st.divider()

    st.subheader("Analysis engine")
    engine_choice = st.radio(
        "Choose evaluation engine",
        ["Built-in Smart Engine", "Google Gemini", "OpenAI"],
        index=0,
        label_visibility="collapsed",
    )

    api_key = ""
    if engine_choice == "Google Gemini":
        api_key = st.text_input("Gemini API key", type="password")
    elif engine_choice == "OpenAI":
        api_key = st.text_input("OpenAI API key", type="password")

    st.divider()
    st.subheader("Try a sample")
    sample_selection = st.selectbox(
        "Candidate profile",
        ["None", "Software Engineer", "AI / ML Engineer"],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="privacy-note">Resume text is processed locally unless you explicitly choose a cloud AI engine.</div>',
        unsafe_allow_html=True,
    )

default_resume_text = ""
default_jd_text = ""
if sample_selection == "Software Engineer":
    try:
        default_resume_text, _ = extract_text_from_file("sample_resumes/sample_software_engineer_resume.txt")
        default_jd_text = PRESET_JOB_DESCRIPTIONS["Full-Stack Software Engineer"]
    except Exception:
        pass
elif sample_selection == "AI / ML Engineer":
    try:
        default_resume_text, _ = extract_text_from_file("sample_resumes/sample_data_scientist_resume.txt")
        default_jd_text = PRESET_JOB_DESCRIPTIONS["Data Scientist & AI / ML Engineer"]
    except Exception:
        pass

st.markdown(
    """
    <div class="hero">
        <h1>Make every application ATS-ready.</h1>
        <p>Audit resume quality, match target requirements, detect duplicated language, and prepare interview-ready improvements.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

resume_col, jd_col = st.columns([1, 1], gap="large")
with resume_col:
    st.markdown('<div class="step-label">1. Candidate resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
    resume_text = ""
    file_meta = {}
    if uploaded_file:
        resume_text, file_meta = extract_text_from_bytes(uploaded_file.read(), uploaded_file.name)
        st.success(f"Loaded {uploaded_file.name} - {file_meta.get('words', 0)} words")
    else:
        resume_text = st.text_area(
            "Resume text",
            value=default_resume_text,
            height=270,
            placeholder="Paste the resume text here...",
            label_visibility="collapsed",
        )

with jd_col:
    st.markdown('<div class="step-label">2. Target role</div>', unsafe_allow_html=True)
    preset_role = st.selectbox(
        "Job description template",
        ["Custom / Paste Below"] + list(PRESET_JOB_DESCRIPTIONS.keys()),
    )
    jd_input_value = PRESET_JOB_DESCRIPTIONS[preset_role] if preset_role != "Custom / Paste Below" else default_jd_text
    jd_text = st.text_area(
        "Job description",
        value=jd_input_value,
        height=270,
        placeholder="Paste the complete job description...",
        label_visibility="collapsed",
    )

reference_col, action_col = st.columns([3, 1], gap="large")
with reference_col:
    with st.expander("Originality check - optional reference text or document"):
        reference_file = st.file_uploader(
            "Upload a reference resume or text",
            type=["pdf", "docx", "txt"],
            key="reference_file",
        )
        reference_text = ""
        if reference_file:
            reference_text, _ = extract_text_from_bytes(reference_file.read(), reference_file.name)
            st.caption(f"Reference loaded: {reference_file.name}")
        reference_text = st.text_area(
            "Or paste reference text",
            value=reference_text,
            height=140,
            placeholder="Paste a reference resume, template, or document for similarity comparison...",
        )
with action_col:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("Analyze resume", type="primary", use_container_width=True)

if analyze_clicked or ("analysis_result" in st.session_state and resume_text):
    if not resume_text or len(resume_text.strip()) < 40:
        st.error("Add a resume with at least 40 characters to begin.")
    else:
        with st.spinner("Running ATS, impact, structure, and originality checks..."):
            analysis = analyze_resume_vs_jd(resume_text, jd_text)
            originality = calculate_originality(resume_text, reference_text)
            provider_type = "gemini" if engine_choice == "Google Gemini" else ("openai" if engine_choice == "OpenAI" else "auto")
            ai_feedback = generate_ai_critique(
                resume_text,
                jd_text,
                analysis,
                api_key.strip() if api_key else None,
                provider_type,
            )
            st.session_state["analysis_result"] = analysis
            st.session_state["ai_feedback"] = ai_feedback
            st.session_state["originality_result"] = originality

        analysis = st.session_state["analysis_result"]
        ai_feedback = st.session_state["ai_feedback"]
        originality = st.session_state["originality_result"]

        st.markdown("---")
        score = analysis["ats_score"]
        if score >= 80:
            score_status, score_color = "Strong match", "#059669"
        elif score >= 65:
            score_status, score_color = "Good match", "#2563eb"
        elif score >= 50:
            score_status, score_color = "Needs work", "#d97706"
        else:
            score_status, score_color = "Major gaps", "#dc2626"

        skill_pct = analysis.get("skill_match_pct", 100 if not analysis["has_jd"] else 0)
        metric_columns = st.columns(5)
        metrics = [
            ("ATS match", f"{score}%", score_status),
            ("Skills match", f"{skill_pct}%", f"{len(analysis.get('matched_skills', []))} matched"),
            ("Quantified impact", f"{analysis['bullets']['quantification_score']}%", f"{analysis['bullets']['quantified_count']} metrics"),
            ("Action strength", f"{analysis['bullets']['action_verb_score']}%", f"{analysis['bullets']['strong_verb_count']} strong verbs"),
            ("Originality", f"{originality['originality_score']}%", originality["status"]),
        ]
        for column, (label, value, detail) in zip(metric_columns, metrics):
            with column:
                color = score_color if label == "ATS match" else "#14213d"
                st.markdown(
                    f'<div class="metric-shell"><div class="label">{label}</div>'
                    f'<div class="value" style="color:{color}">{value}</div>'
                    f'<div class="detail">{detail}</div></div>',
                    unsafe_allow_html=True,
                )

        tab_skills, tab_impact, tab_format, tab_originality, tab_feedback = st.tabs(
            ["Skills & gaps", "Impact & bullets", "ATS structure", "Originality", "Recruiter review"]
        )

        with tab_skills:
            if analysis["has_jd"]:
                matched, missing = st.columns(2)
                with matched:
                    st.subheader("Matched skills")
                    st.write(", ".join(analysis["matched_skills"]) if analysis["matched_skills"] else "No direct matches detected.")
                with missing:
                    st.subheader("Missing skills")
                    st.write(", ".join(analysis["missing_skills"]) if analysis["missing_skills"] else "No major target skills missing.")
                    if analysis["missing_skills"]:
                        st.caption("Add only skills you genuinely possess and can demonstrate.")
            st.divider()
            st.subheader("Detected skill profile")
            for category, skills in analysis["resume_skills"].items():
                with st.expander(f"{category} - {len(skills)}"):
                    st.write(", ".join(skill.title() for skill in skills))

        with tab_impact:
            st.subheader("Bullet impact review")
            left, right = st.columns(2)
            with left:
                st.metric("Strong action verbs", analysis["bullets"]["strong_verb_count"])
            with right:
                st.metric("Passive phrases", analysis["bullets"]["weak_verb_count"])

            for index, rewrite in enumerate(ai_feedback.get("bullet_rewrites", []), 1):
                st.markdown(
                    f'<div class="rewrite-card"><strong>Revision {index}</strong><br>'
                    f'<span style="color:#64748b">Before:</span> {rewrite["original"]}<br><br>'
                    f'<span style="color:#166534;font-weight:700">Recommended:</span> {rewrite["revised"]}<br>'
                    f'<small style="color:#64748b">{rewrite["rationale"]}</small></div>',
                    unsafe_allow_html=True,
                )

        with tab_format:
            st.subheader("ATS structure checklist")
            st.write(f"**Word count:** {analysis['word_count']} | **Reading time:** ~{analysis['reading_time_mins']} min")
            st.caption(analysis["length_feedback"])
            sections_col, contact_col = st.columns(2)
            with sections_col:
                for section, present in analysis["sections"]["sections"].items():
                    st.write(("✅ " if present else "❌ ") + section)
            with contact_col:
                st.markdown("**Detected contact details**")
                contacts = analysis["sections"]["contact_details"]
                st.write(f"Email: {contacts['email']}")
                st.write(f"Phone: {contacts['phone']}")
                st.write(f"LinkedIn: {contacts['linkedin']}")
                st.write(f"GitHub: {contacts['github']}")

        with tab_originality:
            st.subheader("Originality & similarity")
            tone = originality["status_tone"]
            st.markdown(
                f'<span class="status-pill status-{tone}">{originality["status"]}</span>',
                unsafe_allow_html=True,
            )
            st.progress(originality["originality_score"] / 100, text=f"Originality estimate: {originality['originality_score']}%")
            st.caption(
                "This is an offline heuristic comparison. It cannot search the public internet or prove plagiarism."
                if originality["has_reference"]
                else "Paste or upload reference text to enable a reference comparison. Internal repeated-sentence detection is always available."
            )
            if originality["matched_phrases"]:
                st.markdown("**Most similar phrases**")
                for phrase in originality["matched_phrases"]:
                    st.code(phrase)
            if originality["repeated_sentences"]:
                st.markdown("**Repeated sentences**")
                for sentence in originality["repeated_sentences"]:
                    st.write(sentence)

        with tab_feedback:
            st.subheader("Recruiter evaluation")
            st.caption(f"Generated by {ai_feedback.get('engine', 'Smart NLP Engine')}")
            st.markdown(f"**Verdict:** {ai_feedback.get('executive_summary', '')}")
            strengths, improvements = st.columns(2)
            with strengths:
                st.markdown("**Strengths**")
                for item in ai_feedback.get("strengths", []):
                    st.write(f"- {item}")
            with improvements:
                st.markdown("**Priority improvements**")
                for item in ai_feedback.get("improvements", []):
                    st.write(f"- {item}")
            st.divider()
            st.markdown("**Interview preparation**")
            for index, question in enumerate(ai_feedback.get("interview_questions", []), 1):
                st.write(f"{index}. {question}")

        report_md = f"""# ResumeIQ Analysis Report

## Summary
- ATS Match Score: {analysis['ats_score']}%
- Skills Match: {analysis.get('skill_match_pct', 'N/A')}%
- Quantified Impact: {analysis['bullets']['quantification_score']}%
- Action Strength: {analysis['bullets']['action_verb_score']}%
- Originality Estimate: {originality['originality_score']}%
- Similarity Estimate: {originality['similarity_score']}%

## Recruiter Verdict
{ai_feedback.get('executive_summary', '')}

## Matched Skills
{', '.join(analysis.get('matched_skills', [])) or 'None'}

## Missing Skills
{', '.join(analysis.get('missing_skills', [])) or 'None'}

## Bullet Rewrites
"""
        for index, rewrite in enumerate(ai_feedback.get("bullet_rewrites", []), 1):
            report_md += f"\n### Revision {index}\n- Before: {rewrite['original']}\n- Recommended: {rewrite['revised']}\n"

        st.download_button(
            "Download analysis report",
            data=report_md,
            file_name="resumeiq_analysis_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
