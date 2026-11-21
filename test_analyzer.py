"""Quick smoke test for analyzer components."""
from analyzer.parser import extract_text_from_file
from analyzer.nlp_engine import analyze_resume_vs_jd, calculate_originality
from analyzer.ai_client import generate_ai_critique
from analyzer.templates import PRESET_JOB_DESCRIPTIONS

def test_pipeline():
    sample_file = "sample_resumes/sample_software_engineer_resume.txt"
    text, meta = extract_text_from_file(sample_file)
    print(f"Extracted {meta['words']} words, type: {meta['type']}")
    assert meta["words"] > 100, "Text extraction failed!"

    jd = PRESET_JOB_DESCRIPTIONS["Full-Stack Software Engineer"]
    analysis = analyze_resume_vs_jd(text, jd)

    print("\n--- ANALYSIS RESULTS ---")
    print(f"ATS Score: {analysis['ats_score']}%")
    print(f"Skill Match: {analysis['skill_match_pct']}%")
    print(f"Matched Skills ({len(analysis['matched_skills'])}): {analysis['matched_skills']}")
    print(f"Missing Skills ({len(analysis['missing_skills'])}): {analysis['missing_skills']}")
    print(f"Quantification Score: {analysis['bullets']['quantification_score']}%")
    print(f"Strong Verbs Used: {analysis['bullets']['strong_verbs_found']}")

    critique = generate_ai_critique(text, jd, analysis)
    print("\n--- AI CRITIQUE ---")
    print("Engine:", critique["engine"])
    print("Verdict:", critique["executive_summary"])
    print("Strengths:", len(critique["strengths"]))
    print("Improvements:", len(critique["improvements"]))
    print("Rewrites:", len(critique["bullet_rewrites"]))

    reference = "We are looking for a Python engineer with Python, Docker, AWS and strong communication skills."
    originality = calculate_originality(text, reference)
    print("Similarity:", originality["similarity_score"])
    print("Originality:", originality["originality_score"])

    print("\n[SUCCESS] All components verified cleanly!")

if __name__ == "__main__":
    test_pipeline()
