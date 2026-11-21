#!/usr/bin/env python3
"""
CLI Interface for AI Resume Analyser
Run:
    python cli.py --resume sample_resumes/sample_software_engineer_resume.txt --role "Full-Stack Software Engineer"
"""
import argparse
import sys
from analyzer.parser import extract_text_from_file
from analyzer.nlp_engine import analyze_resume_vs_jd
from analyzer.ai_client import generate_ai_critique
from analyzer.templates import PRESET_JOB_DESCRIPTIONS

def main():
    parser = argparse.ArgumentParser(description="AI Resume Analyser CLI")
    parser.add_argument("--resume", "-r", required=True, help="Path to resume file (.pdf, .docx, or .txt)")
    parser.add_argument("--jd", "-j", help="Path to job description file (.txt)")
    parser.add_argument("--role", help="Preset role name: 'Full-Stack Software Engineer', 'Data Scientist & AI / ML Engineer', 'DevOps & Cloud Engineer', 'Product Manager (Tech)'")
    parser.add_argument("--api-key", help="Optional Google Gemini or OpenAI API Key")
    parser.add_argument("--output", "-o", help="Optional output markdown file path")

    args = parser.parse_args()

    print(f"\n[+] Loading resume from: {args.resume}")
    try:
        resume_text, meta = extract_text_from_file(args.resume)
    except Exception as e:
        print(f"[!] Error loading resume: {e}")
        sys.exit(1)

    jd_text = ""
    if args.role and args.role in PRESET_JOB_DESCRIPTIONS:
        print(f"[+] Using preset role template: {args.role}")
        jd_text = PRESET_JOB_DESCRIPTIONS[args.role]
    elif args.jd:
        print(f"[+] Loading JD from: {args.jd}")
        try:
            with open(args.jd, "r", encoding="utf-8") as f:
                jd_text = f.read()
        except Exception as e:
            print(f"[!] Error reading JD: {e}")
            sys.exit(1)

    print("[*] Analyzing resume and matching skills...")
    analysis = analyze_resume_vs_jd(resume_text, jd_text)
    critique = generate_ai_critique(resume_text, jd_text, analysis, api_key=args.api_key)

    print("\n" + "=" * 50)
    print("           AI RESUME ANALYSIS RESULTS")
    print("=" * 50)
    print(f"ATS Match Score:        {analysis['ats_score']}%")
    if analysis.get('has_jd'):
        print(f"Skills Match:           {analysis['skill_match_pct']}%")
    print(f"Quantification Score:   {analysis['bullets']['quantification_score']}%")
    print(f"Action Verb Score:      {analysis['bullets']['action_verb_score']}%")
    print(f"Total Words:            {analysis['word_count']} words")
    print(f"Length Check:           {analysis['length_feedback']}")
    print("-" * 50)

    if analysis.get('has_jd'):
        print(f"\n[+] Matched Skills ({len(analysis['matched_skills'])}):")
        print("    " + ", ".join(analysis['matched_skills']))
        print(f"\n[-] Missing Target Skills ({len(analysis['missing_skills'])}):")
        print("    " + ", ".join(analysis['missing_skills']))

    print(f"\n[+] Strong Verbs Detected ({len(analysis['bullets']['strong_verbs_found'])}):")
    print("    " + ", ".join(analysis['bullets']['strong_verbs_found']))

    if analysis['bullets']['weak_verbs_found']:
        print(f"\n[!] Weak Verbs to Replace:")
        print("    " + ", ".join(analysis['bullets']['weak_verbs_found']))

    print("\n" + "=" * 50)
    print(f"RECRUITER FEEDBACK ({critique.get('engine', 'Built-in Engine')})")
    print("=" * 50)
    print(f"Verdict: {critique.get('executive_summary', '')}\n")

    print("Candidate Strengths:")
    for s in critique.get("strengths", []):
        print(f"  * {s}")

    print("\nActionable Improvements:")
    for imp in critique.get("improvements", []):
        print(f"  * {imp}")

    print("\nHigh-Impact Bullet Point Rewrites:")
    for i, r in enumerate(critique.get("bullet_rewrites", []), 1):
        print(f"\n  Bullet #{i}:")
        print(f"    Original: {r['original']}")
        print(f"    Revised:  {r['revised']}")
        print(f"    Why:      {r['rationale']}")

    print("\nInterview Questions to Anticipate:")
    for i, q in enumerate(critique.get("interview_questions", []), 1):
        print(f"  Q{i}: {q}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"# AI Resume Analysis Report\n\nScore: {analysis['ats_score']}%\n\nVerdict: {critique.get('executive_summary')}\n")
        print(f"\n[+] Saved report to {args.output}")

if __name__ == "__main__":
    main()
