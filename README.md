# 📄 AI Resume Analyser & ATS Optimizer

A lightweight, professional resume checker and ATS (Applicant Tracking System) optimizer built with Python and FastAPI, ready to deploy on Vercel.

It audits resumes against Job Descriptions, detects technical and soft skill gaps, evaluates quantifiable business impact, flags passive verbs, verifies standard ATS formatting, and produces recruiter-level feedback with AI-powered bullet point rewrites.

ResumeIQ also includes an originality check. Upload or paste reference text for similarity comparison, with repeated-sentence detection available even without a reference. It is a heuristic signal and does not search or prove results across the public internet.

---

## ✨ Features

- **Multi-Format Resume Ingestion**: Upload resumes in **PDF** (`.pdf`), Microsoft Word (**DOCX** `.docx`), or Plain Text (**TXT** `.txt`), or paste text directly.
- **ATS Compatibility Scoring**: Composite score (0 - 100%) computed across:
  - Technical & Soft Skill Overlap (40%)
  - Keyword & Vocabulary Density (25%)
  - Quantified Impact Metrics (15%)
  - Action Verb Strength (10%)
  - Standard Section Completeness (10%)
- **Skills & Keyword Gap Analysis**:
  - Matched skills badges (Green)
  - Missing required job skills (Red/Orange) to add before applying
  - Extra candidate skills
  - Organized categorization (Languages, Frameworks, Cloud/DevOps, Databases, Data/AI, Methodologies)
- **Impact & Bullet Point Revamp**:
  - Quantifiable metrics detection (dollar amounts, percentages, user scale, speed multipliers)
  - Strong action verbs identified (*Architected, Spearheaded, Optimized*) vs weak verbs to eliminate (*Worked on, Helped*)
  - **Before & After AI Bullet Rewrites** following the formula: `[Action Verb] + [Context/Project] + [Measurable Outcome]`
- **ATS Formatting & Structure Checklist**:
  - Automatically verifies essential sections: Contact Information, Summary, Work Experience, Education, Skills, and Projects
  - Extracts email, phone number, LinkedIn, and GitHub links
- **Recruiter Evaluation & Interview Prep**:
  - Executive recruiter verdict
  - Top strengths and high-priority recommendations
  - Tailored interview questions probing skill gaps
- **Dual AI Engine**:
  - **Built-in Smart NLP Engine**: No third-party AI key required.
  - **Cloud LLM Support (Optional)**: Enter a Google Gemini or OpenAI API key for deeper custom critiques.
- **Export Reports**: 1-click download of comprehensive analysis reports in Markdown.
- **CLI Utility**: Terminal-based analysis tool for rapid workflows.

---

## 🚀 Quickstart

### 1. Requirements & Installation

Ensure you have Python 3.10+ installed.

```bash
cd d:\AI_Resume_Analyser
pip install -r requirements.txt
```

### 2. Launch the Web Interface

**On Windows:**
Double-click `run.bat` or run:

```bash
python -m uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

### 3. Deploy to Vercel

The Vercel Python runtime loads the FastAPI `app` exported from the root `app.py`. The `requirements.txt` file includes the API dependencies, and Vercel serves the UI from `static/index.html`.

1. Import this GitHub repository into Vercel.
2. Leave the framework preset on **Other** or allow Vercel to detect Python.
3. Use the root directory; no build command or output directory is required.
4. Deploy the project. The app should open at the deployment URL.

Do not configure `app.py` as a Streamlit command or add a placeholder handler; it is now a FastAPI ASGI entrypoint.

---

## 💻 CLI Usage

You can also run resume audits directly from your terminal:

```bash
# Analyze a resume against a pre-defined role template:
python cli.py --resume sample_resumes/sample_software_engineer_resume.txt --role "Full-Stack Software Engineer"

# Analyze a resume against a custom job description file:
python cli.py --resume path/to/my_resume.pdf --jd path/to/job_description.txt --output report.md
```

Available preset roles:
- `"Full-Stack Software Engineer"`
- `"Data Scientist & AI / ML Engineer"`
- `"DevOps & Cloud Engineer"`
- `"Product Manager (Tech)"`

---

## 📂 Project Architecture

```
AI_Resume_Analyser/
├── app.py                  # FastAPI/Vercel entrypoint and analysis API
├── static/index.html       # ResumeIQ web interface
├── cli.py                  # Terminal command-line interface
├── run.bat                 # 1-click Windows launcher
├── run.ps1                 # PowerShell launcher
├── requirements.txt        # Dependencies (FastAPI, Uvicorn, parsers, requests)
├── test_analyzer.py        # Automated test suite
├── analyzer/
│   ├── __init__.py         # Package entrypoint
│   ├── parser.py           # PDF, DOCX, and TXT extractors
│   ├── nlp_engine.py       # Skill taxonomy, keyword matching, ATS scoring
│   ├── ai_client.py        # Gemini / OpenAI REST connector + Offline smart generator
│   └── templates.py        # Curated industry job description templates
└── sample_resumes/
    ├── sample_software_engineer_resume.txt
    └── sample_data_scientist_resume.txt
```

---

## 🔑 AI Engine Configuration (Optional)

- **Default (No API Key Required)**: The app uses its built-in rule and NLP engine.
- **Google Gemini**: Get a key from [Google AI Studio](https://aistudio.google.com/) and enter it for an analysis.
- **OpenAI**: Enter your OpenAI API key for an analysis.

When deployed, resume and reference text are sent to the Vercel function for analysis; this app does not write them to a database or file. Selecting Gemini or OpenAI also sends resume and job-description text to the selected provider. API keys are sent with the analysis request and must never be committed to the repository.
