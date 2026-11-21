import os
import json
import requests
from typing import Dict, Any, Optional

def generate_ai_critique(
    resume_text: str,
    jd_text: str,
    analysis_data: Dict[str, Any],
    api_key: Optional[str] = None,
    provider: str = "auto"
) -> Dict[str, Any]:
    """
    Generates high-level executive recruiter critique, bullet rewrites, and interview questions.
    If an API key is provided, calls Google Gemini or OpenAI.
    Otherwise, leverages the rule-based expert intelligence engine to generate full structured feedback!
    """
    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")

    if key:
        # Check provider type
        if "AIza" in key or provider == "gemini":
            ai_result = _call_gemini_api(key, resume_text, jd_text, analysis_data)
            if ai_result:
                return ai_result
        elif key.startswith("sk-") or provider == "openai":
            ai_result = _call_openai_api(key, resume_text, jd_text, analysis_data)
            if ai_result:
                return ai_result

    # Fallback to Built-in Rule Engine (100% works without any keys!)
    return _generate_smart_heuristic_critique(resume_text, jd_text, analysis_data)

def _generate_smart_heuristic_critique(
    resume_text: str,
    jd_text: str,
    analysis_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Produces deterministic, intelligent recruiter-grade insights when no LLM key is configured.
    """
    score = analysis_data.get("ats_score", 70)
    matched = analysis_data.get("matched_skills", [])
    missing = analysis_data.get("missing_skills", [])
    bullets = analysis_data.get("bullets", {})
    sections = analysis_data.get("sections", {}).get("sections", {})
    weak_verbs = bullets.get("weak_verbs_found", [])

    # Grade
    if score >= 85:
        verdict = "Excellent Match - Strong candidate for recruiter screen."
    elif score >= 70:
        verdict = "Good Foundation - Minor keyword and impact tuning recommended."
    elif score >= 50:
        verdict = "Moderate Match - Notable skill gaps and weak quantification."
    else:
        verdict = "Needs Major Optimization - Misaligned with targeted requirements."

    # Strengths
    strengths = []
    if matched:
        strengths.append(f"Demonstrated alignment in core technical stack: {', '.join(matched[:5])}.")
    if bullets.get("quantified_count", 0) >= 3:
        strengths.append("Contains measurable business outcomes (metrics, dollar figures, or percentages).")
    if bullets.get("strong_verb_count", 0) >= 4:
        strengths.append(f"Effective use of authoritative action verbs ({', '.join(bullets.get('strong_verbs_found', [])[:4])}).")
    if sections.get("Work Experience") and sections.get("Skills"):
        strengths.append("Clear structural organization with designated Work Experience and Technical Skills sections.")
    if not strengths:
        strengths.append("Foundational technical background present; ready for narrative enhancement.")

    # Weaknesses / Improvements
    improvements = []
    if missing:
        improvements.append(f"Critical Missing Keywords: Add direct experience or project context with {', '.join(missing[:6])}.")
    if bullets.get("quantification_score", 0) < 50:
        improvements.append("Insufficient Metric Quantification: Add numbers (e.g., latency reduction %, scale, revenue impact).")
    if weak_verbs:
        improvements.append(f"Passive Verb Usage: Replace passive phrases like '{', '.join(weak_verbs[:3])}' with assertive verbs (e.g., Architected, Engineered, Spearheaded).")
    for sec_name, present in sections.items():
        if not present:
            improvements.append(f"Missing Essential Section: Please add a dedicated '{sec_name}' section for ATS parsers.")
    if not improvements:
        improvements.append("Tailor bullet points to mirror exact terminology from the target company's job posting.")

    # High-impact Bullet Point Rewrites
    samples = bullets.get("samples", [])
    # Pick bullets to improve: prioritize those lacking metrics or using weak verbs
    target_bullets = [s for s in samples if (not s.get("has_metric") or s.get("is_weak")) and len(s.get("text", "")) > 25]
    if len(target_bullets) < 3:
        target_bullets.extend([s for s in samples if s not in target_bullets and len(s.get("text", "")) > 25])

    rewrites = []
    enhancement_templates = [
        ("improving system performance by 35% and supporting 50,000+ concurrent requests", "Added concrete performance metrics and user scale indicators to demonstrate business value."),
        ("reducing data processing latency by 42% across multi-region production clusters", "Transformed broad technical description into quantifiable outcome with SLA impact."),
        ("accelerating delivery velocity by 30% and eliminating high-priority production incidents", "Replaced task-oriented language with measurable reliability and velocity results.")
    ]

    for i in range(min(3, len(target_bullets))):
        orig = target_bullets[i]["text"]
        metric_add, rationale = enhancement_templates[i]

        # Dynamic rewrite logic
        revised = orig
        # Clean weak verbs if present
        for wv in ["was responsible for", "responsible for", "assisted with", "worked on", "helped", "handled"]:
            if orig.lower().startswith(wv):
                revised = orig[len(wv):].strip(" ,")
                break
        
        # Ensure capitalization and add strong action verb if needed
        words = revised.split()
        if words and words[0].lower() not in [
            "architected", "spearheaded", "engineered", "built", "developed", 
            "deployed", "automated", "optimized", "mentored", "conducted", "led", "managed"
        ]:
            revised = f"Spearheaded and delivered {revised[0].lower() + revised[1:]}"
        else:
            revised = revised[0].upper() + revised[1:]

        # If original didn't have a metric, append a strong metric outcome
        if not target_bullets[i].get("has_metric"):
            revised = f"{revised.rstrip('.')}, {metric_add}."
        else:
            revised = f"{revised.rstrip('.')}."

        rewrites.append({
            "original": orig,
            "revised": revised,
            "rationale": rationale
        })

    # If no bullets detected
    if not rewrites:
        rewrites = [
            {
                "original": "Worked on web application development and bug fixes.",
                "revised": "Architected high-throughput services and interactive features, reducing API response times by 32% for 50,000+ daily active users.",
                "rationale": "Replaced generic task description with authoritative action verb ('Architected') and measurable business impact."
            }
        ]

    # Recruiter Interview Questions
    interview_questions = []
    if missing:
        interview_questions.append(f"We noticed {missing[0]} is prominent in our JD. Can you walk us through your familiarity with it or how you'd ramp up quickly?")
    if matched:
        interview_questions.append(f"Tell us about the most complex challenge you solved while working with {matched[0]}.")
    interview_questions.append("Can you quantify the single highest-impact technical project you led in your recent role?")
    interview_questions.append("Walk us through an architectural trade-off decision you made when scaling an application under tight deadlines.")

    return {
        "engine": "Built-in Intelligent Rule Engine (Offline / Instant)",
        "executive_summary": verdict,
        "strengths": strengths[:4],
        "improvements": improvements[:4],
        "bullet_rewrites": rewrites,
        "interview_questions": interview_questions[:4]
    }

def _call_gemini_api(api_key: str, resume_text: str, jd_text: str, analysis_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Calls Google Gemini REST API using requests."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""You are an elite Fortune 500 Executive Recruiter and ATS Optimization Expert.
Analyze this resume against the target job description.

RESUME TEXT:
{resume_text[:4000]}

JOB DESCRIPTION:
{jd_text[:2500] if jd_text else "General Evaluation"}

ATS Match Score calculated: {analysis_data.get('ats_score', 75)}%
Missing Skills: {analysis_data.get('missing_skills', [])}

Return a valid JSON object strictly matching this schema:
{{
    "executive_summary": "2-3 sentence recruiter impression of the candidate",
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "improvements": ["improvement 1", "improvement 2", "improvement 3"],
    "bullet_rewrites": [
        {{
            "original": "Exact or approximate weak bullet point from the resume",
            "revised": "High-impact rewrite following: Action Verb + Context + Quantified Metric/Outcome",
            "rationale": "Why this revision performs significantly better for ATS and hiring managers"
        }}
    ],
    "interview_questions": [
        "Question 1 probing candidate's biggest skill gap or key project",
        "Question 2 probing technical architecture decision",
        "Question 3 probing leadership and impact"
    ]
}}
Respond with ONLY the JSON object, without backticks or markdown fences.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            raw_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
            # Clean possible markdown wrap
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            parsed = json.loads(raw_text.strip())
            parsed["engine"] = "Google Gemini 1.5 Flash"
            return parsed
    except Exception:
        pass
    return None

def _call_openai_api(api_key: str, resume_text: str, jd_text: str, analysis_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Calls OpenAI REST API using requests."""
    url = "https://api.openai.com/v1/chat/completions"
    
    prompt = f"""You are an elite Fortune 500 Executive Recruiter and ATS Optimization Expert.
Analyze this resume against the target job description.

RESUME TEXT:
{resume_text[:4000]}

JOB DESCRIPTION:
{jd_text[:2500] if jd_text else "General Evaluation"}

ATS Match Score: {analysis_data.get('ats_score', 75)}%

Return a valid JSON object matching:
{{
    "executive_summary": "Recruiter evaluation summary",
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "improvements": ["improvement 1", "improvement 2", "improvement 3"],
    "bullet_rewrites": [
        {{
            "original": "weak bullet",
            "revised": "strong rewrite with metrics",
            "rationale": "explanation"
        }}
    ],
    "interview_questions": ["q1", "q2", "q3"]
}}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a specialized JSON-only resume analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            raw_text = data['choices'][0]['message']['content'].strip()
            parsed = json.loads(raw_text)
            parsed["engine"] = "OpenAI GPT-4o-mini"
            return parsed
    except Exception:
        pass
    return None
