# 📄 AI Resume Analyser & ATS Optimizer

A lightweight, modern AI-powered Resume Analyser and ATS (Applicant Tracking System) Optimizer built with Python and Streamlit.

It audits resumes against Job Descriptions, detects technical and soft skill gaps, evaluates quantifiable business impact, flags passive verbs, verifies standard ATS formatting, and produces recruiter-level feedback with AI-powered bullet point rewrites.

ResumeIQ also includes a privacy-first originality check. Upload or paste reference text for local similarity comparison, with repeated-sentence detection available even without a reference. It is a heuristic signal and does not claim to search or prove results across the public internet.

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
  - **Built-in Smart NLP Engine**: Works 100% offline with zero setup and no API keys needed!
  - **Cloud LLM Support (Optional)**: Enter your Google Gemini or OpenAI API key directly in the sidebar for deeper custom critiques.
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
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

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
├── app.py                  # Streamlit web application & interactive UI
├── cli.py                  # Terminal command-line interface
├── run.bat                 # 1-click Windows launcher
├── run.ps1                 # PowerShell launcher
├── requirements.txt        # Dependencies (streamlit, pypdf, python-docx, requests)
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

- **Default (No API Key Required)**: The app runs with its built-in rule and NLP engine immediately.
- **Google Gemini**: Get a free API key from [Google AI Studio](https://aistudio.google.com/) and paste it into the sidebar or set `GEMINI_API_KEY=your_key`.
- **OpenAI**: Paste your OpenAI key into the sidebar or set `OPENAI_API_KEY=your_key`.
