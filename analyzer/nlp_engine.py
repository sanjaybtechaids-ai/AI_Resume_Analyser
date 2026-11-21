import re
from typing import Dict, List, Set, Any, Tuple

# Comprehensive taxonomy of industry skills
SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "golang", "go",
        "rust", "ruby", "php", "swift", "kotlin", "sql", "html", "html5", "css", "css3",
        "r", "scala", "dart", "bash", "shell", "powershell", "perl", "matlab"
    ],
    "Frameworks & Libraries": [
        "react", "react.js", "next.js", "vue", "vue.js", "angular", "node.js", "express",
        "express.js", "django", "flask", "fastapi", "spring", "spring boot", "asp.net",
        ".net", "laravel", "tailwind", "tailwind css", "bootstrap", "redux", "graphql",
        "rest api", "restful", "grpc", "pytorch", "tensorflow", "keras", "scikit-learn",
        "pandas", "numpy", "opencv", "huggingface", "transformers", "langchain",
        "llamaindex", "jquery", "flutter", "react native"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "gcp", "google cloud", "docker",
        "kubernetes", "k8s", "terraform", "ansible", "jenkins", "git", "github",
        "github actions", "gitlab", "ci/cd", "continuous integration", "continuous deployment",
        "linux", "nginx", "apache", "helm", "prometheus", "grafana", "datadog",
        "serverless", "lambda", "microservices"
    ],
    "Databases & Storage": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "sqlite", "oracle", "snowflake", "bigquery",
        "firebase", "supabase", "mariadb", "neo4j", "chromadb", "pinecone"
    ],
    "Data & AI": [
        "machine learning", "deep learning", "artificial intelligence", "nlp",
        "natural language processing", "computer vision", "generative ai", "llm",
        "large language models", "etl", "data engineering", "spark", "apache spark",
        "hadoop", "kafka", "tableau", "power bi", "a/b testing", "data analysis",
        "statistical analysis", "predictive modeling"
    ],
    "Soft Skills & Methodologies": [
        "agile", "scrum", "kanban", "leadership", "communication", "teamwork",
        "problem solving", "critical thinking", "mentoring", "mentorship",
        "cross-functional collaboration", "stakeholder management", "project management",
        "time management", "analytical thinking", "system design"
    ]
}

# Strong action verbs favored by ATS and hiring managers
STRONG_ACTION_VERBS = [
    "accelerated", "achieved", "acquired", "administered", "advanced", "advised",
    "allocated", "analyzed", "appraised", "architected", "assembled", "audited",
    "automated", "boosted", "budgeted", "built", "centralized", "championed",
    "collaborated", "completed", "composed", "conceived", "conducted", "consolidated",
    "constructed", "consulted", "contracted", "converted", "coordinated", "created",
    "curated", "customized", "debugged", "decreased", "defined", "delegated",
    "delivered", "demonstrated", "deployed", "designed", "developed", "devised",
    "diagnosed", "directed", "discovered", "documented", "doubled", "drafted",
    "drove", "earned", "eliminated", "enabled", "enacted", "engineered",
    "enhanced", "established", "estimated", "evaluated", "exceeded", "executed",
    "expanded", "expedited", "fabricated", "facilitated", "forecasted", "formulated",
    "founded", "generated", "governed", "guided", "halted", "headed", "identified",
    "implemented", "improved", "increased", "initiated", "innovated", "inspected",
    "installed", "instituted", "instructed", "integrated", "intensified", "interpreted",
    "interviewed", "introduced", "invented", "investigated", "launched", "lead",
    "led", "leveraged", "managed", "maximized", "measured", "mediated", "mentored",
    "merged", "migrated", "minimized", "modeled", "moderated", "modernized",
    "monitored", "motivated", "navigated", "negotiated", "obtained", "operated",
    "optimized", "orchestrated", "organized", "originated", "overhauled", "oversaw",
    "partnered", "performed", "pioneered", "planned", "positioned", "prepared",
    "presented", "prioritized", "produced", "programmed", "promoted", "proposed",
    "published", "rebuilt", "recommended", "reconciled", "recruited", "redesigned",
    "reduced", "refined", "refactored", "remodeled", "reorganized", "replaced",
    "rescued", "researched", "resolved", "restructured", "revamped", "reviewed",
    "revitalized", "saved", "scaled", "scheduled", "screened", "secured", "selected",
    "separated", "shaped", "simplified", "solved", "spearheaded", "standardized",
    "steered", "streamlined", "strengthened", "structured", "succeeded", "supervised",
    "surpassed", "synthesized", "systematized", "targeted", "trained", "transformed",
    "translated", "tripled", "troubleshot", "unified", "unlocked", "upgraded",
    "utilized", "validated", "verified", "visualized", "won", "yielded"
]

WEAK_ACTION_VERBS = [
    "worked on", "assisted with", "helped", "handled", "was responsible for",
    "responsible for", "participated in", "attempted", "did", "tasked with",
    "was part of", "tried to", "aided", "supported"
]

def calculate_originality(text: str, reference_text: str = "") -> Dict[str, Any]:
    """
    Calculates reference similarity and internal repetition for a local originality review.
    This is a heuristic, not a substitute for a commercial plagiarism database.
    """
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    words = normalized.split()

    def shingles(items: List[str], size: int = 5) -> Set[str]:
        if len(items) < size:
            return {" ".join(items)} if items else set()
        return {" ".join(items[i:i + size]) for i in range(len(items) - size + 1)}

    resume_shingles = shingles(words)

    reference_similarity = 0
    matched_phrases: List[str] = []
    if reference_text and reference_text.strip():
        ref_normalized = re.sub(r"[^a-z0-9]+", " ", reference_text.lower()).strip()
        ref_words = ref_normalized.split()
        ref_shingles = shingles(ref_words)
        if resume_shingles and ref_shingles:
            overlap = resume_shingles.intersection(ref_shingles)
            jaccard = len(overlap) / max(1, len(resume_shingles.union(ref_shingles)))
            reference_similarity = min(100, round(jaccard * 100 * 4))
            matched_phrases = sorted(list(overlap), key=len, reverse=True)[:5]

    sentences = re.findall(r"[^.!?\n]+[.!?]?|\n", text)
    counts: Dict[str, int] = {}
    for sentence in sentences:
        cleaned = re.sub(r"\s+", " ", re.sub(r"[^a-zA-Z0-9]+", " ", sentence)).strip().lower()
        if len(cleaned.split()) >= 5:
            counts[cleaned] = counts.get(cleaned, 0) + 1

    repeated_sentences = [sentence for sentence, count in counts.items() if count > 1]
    repetition_ratio = (len(repeated_sentences) / max(1, len(counts))) if counts else 0
    repetition_similarity = min(100, round(repetition_ratio * 100))
    similarity_score = min(100, max(reference_similarity, repetition_similarity))

    if similarity_score >= 40:
        status = "High similarity"
        status_tone = "red"
    elif similarity_score >= 20:
        status = "Review recommended"
        status_tone = "amber"
    else:
        status = "Likely original"
        status_tone = "green"

    return {
        "similarity_score": similarity_score,
        "originality_score": 100 - similarity_score,
        "status": status,
        "status_tone": status_tone,
        "reference_similarity": reference_similarity,
        "repeated_sentence_count": len(repeated_sentences),
        "matched_phrases": matched_phrases,
        "repeated_sentences": repeated_sentences[:5],
        "has_reference": bool(reference_text and reference_text.strip())
    }

def extract_skills_from_text(text: str) -> Dict[str, List[str]]:
    """
    Extracts identified technical and soft skills grouped by category.
    """
    text_lower = f" {text.lower()} "
    found_by_category = {}

    for category, skill_list in SKILL_TAXONOMY.items():
        found = []
        for skill in skill_list:
            # Match word boundary for clean skill matching
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                found.append(skill)
        if found:
            found_by_category[category] = sorted(list(set(found)))

    return found_by_category

def flatten_skills(skills_by_cat: Dict[str, List[str]]) -> Set[str]:
    """Combines all categorized skills into a unified lowercase set."""
    flattened = set()
    for skills in skills_by_cat.values():
        for s in skills:
            flattened.add(s.lower())
    return flattened

def check_resume_sections(text: str) -> Dict[str, Any]:
    """
    Checks for essential ATS resume sections and contact information.
    """
    text_lower = text.lower()
    
    # Section presence checks
    sections = {
        "Contact Information": bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text) or re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)),
        "Summary / Objective": bool(re.search(r'\b(summary|professional summary|executive summary|profile|objective|about me)\b', text_lower)),
        "Work Experience": bool(re.search(r'\b(experience|work experience|employment history|professional experience|career history)\b', text_lower)),
        "Education": bool(re.search(r'\b(education|academic background|degree|university|college|bachelor|master|phd)\b', text_lower)),
        "Skills": bool(re.search(r'\b(skills|technical skills|technologies|competencies|expertise|proficiencies)\b', text_lower)),
        "Projects / Certifications": bool(re.search(r'\b(projects|key projects|certifications|certificates|licenses|portfolio)\b', text_lower))
    }

    # Extract contact details if present
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phones = re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    linkedin = re.findall(r'linkedin\.com/in/[\w\-_]+', text_lower)
    github = re.findall(r'github\.com/[\w\-_]+', text_lower)

    found_count = sum(1 for present in sections.values() if present)
    section_score = round((found_count / len(sections)) * 100)

    return {
        "sections": sections,
        "section_score": section_score,
        "contact_details": {
            "email": emails[0] if emails else "Not detected",
            "phone": phones[0] if phones else "Not detected",
            "linkedin": f"https://{linkedin[0]}" if linkedin else "Not detected",
            "github": f"https://{github[0]}" if github else "Not detected"
        }
    }

def evaluate_bullet_points(text: str) -> Dict[str, Any]:
    """
    Analyzes bullet points for strong action verbs, weak verbs, and quantifiable metrics.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Filter to true experience/project bullet points
    bullet_lines = []
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()
        
        # Skip contact / links
        if "@" in line_clean or "linkedin.com" in line_lower or "github.com" in line_lower or re.search(r'\d{3}[-\.\s]\d{3}[-\.\s]\d{4}', line_clean):
            continue
        # Skip lines containing category colons like "Languages:", "Frameworks & Libraries:", "Databases:"
        if re.match(r'^[a-zA-Z\s&/]+\s*:\s*.+', line_clean) and not line_clean.startswith(('-', '•', '*', '–', '—')):
            continue
        # Skip all caps headings like "PROFESSIONAL SUMMARY", "WORK EXPERIENCE"
        if line_clean.isupper() and len(line_clean.split()) <= 4:
            continue
        # Skip role header lines like "Software Engineer | NexaTech Solutions | June 2022 – Present"
        if "|" in line_clean:
            continue

        # Skip skill listing lines even if prefixed with '-'
        if ":" in line_clean:
            prefix = line_clean.split(":")[0].strip("-•*–— ").lower()
            if any(k in prefix for k in [
                "language", "framework", "library", "cloud", "devops", "database",
                "methodolog", "tool", "concept", "ml", "ai", "skills", "data", "education"
            ]):
                continue

        # Valid bullet points start with bullet symbol, number, or strong action verb
        if line_clean.startswith(('-', '•', '*', '–', '—', '1.', '2.', '3.', '4.', '5.')):
            bullet_lines.append(line_clean)
        elif any(line_lower.startswith(v) for v in STRONG_ACTION_VERBS) and len(line_clean.split()) >= 4:
            bullet_lines.append(line_clean)

    # Metric regex: finds percentages, currency ($10M, 50k), numbers, multipliers (2x, 5x)
    metric_pattern = r'(\b\d+(\.\d+)?%|\$\s?\d+[\d,]*(\.\d+)?[kmbKMB]?|\b\d+[\d,]*\+?\s?(users|clients|customers|projects|leads|servers|requests|nodes|teams|people|members|percent)|\b\d+x\b|\b\d{2,}\b)'
    
    total_bullets = len(bullet_lines)
    quantified_bullets = 0
    strong_verb_count = 0
    weak_verb_count = 0
    strong_verbs_used = set()
    weak_verbs_used = set()

    evaluated_bullets = []

    for line in bullet_lines[:30]:
        line_clean = line.lstrip('-•*–— 0123456789.').strip()
        words = line_clean.lower().split()
        first_words = " ".join(words[:3]) if words else ""
        
        has_metric = bool(re.search(metric_pattern, line_clean, re.IGNORECASE))
        if has_metric:
            quantified_bullets += 1

        is_strong = False
        is_weak = False

        for verb in STRONG_ACTION_VERBS:
            if re.search(r'\b' + re.escape(verb) + r'\b', first_words):
                strong_verb_count += 1
                strong_verbs_used.add(verb)
                is_strong = True
                break
        
        for wverb in WEAK_ACTION_VERBS:
            if wverb in line_clean.lower():
                weak_verb_count += 1
                weak_verbs_used.add(wverb)
                is_weak = True
                break

        evaluated_bullets.append({
            "text": line_clean,
            "has_metric": has_metric,
            "is_strong": is_strong,
            "is_weak": is_weak
        })

    # Calculations
    quant_score = min(100, round((quantified_bullets / max(1, total_bullets)) * 140))
    action_verb_score = min(100, round((strong_verb_count / max(1, total_bullets)) * 120))
    if weak_verb_count > 0:
        action_verb_score = max(0, action_verb_score - (weak_verb_count * 5))

    return {
        "total_bullet_points": total_bullets,
        "quantified_count": quantified_bullets,
        "quantification_score": quant_score,
        "strong_verb_count": strong_verb_count,
        "weak_verb_count": weak_verb_count,
        "action_verb_score": action_verb_score,
        "strong_verbs_found": sorted(list(strong_verbs_used)),
        "weak_verbs_found": sorted(list(weak_verbs_used)),
        "samples": evaluated_bullets[:8]
    }

def analyze_resume_vs_jd(resume_text: str, jd_text: str = "") -> Dict[str, Any]:
    """
    Performs full ATS and NLP matching between Resume and optional Job Description.
    """
    resume_skills_by_cat = extract_skills_from_text(resume_text)
    resume_skills_flat = flatten_skills(resume_skills_by_cat)

    sections_info = check_resume_sections(resume_text)
    bullet_info = evaluate_bullet_points(resume_text)

    # Word count and reading time
    word_count = len(re.findall(r'\b\w+\b', resume_text))
    read_time_mins = max(1, round(word_count / 220, 1))

    # Length Evaluation
    if word_count < 250:
        length_feedback = "Too Short (under 250 words). May lack sufficient technical depth."
    elif 300 <= word_count <= 800:
        length_feedback = "Optimal Length (1 - 2 pages, standard ATS target)."
    elif 800 < word_count <= 1400:
        length_feedback = "Good for Senior / Executive positions (2 pages)."
    else:
        length_feedback = "Potentially Too Long (>1400 words). Consider trimming to 2 focused pages."

    result = {
        "word_count": word_count,
        "reading_time_mins": read_time_mins,
        "length_feedback": length_feedback,
        "resume_skills": resume_skills_by_cat,
        "resume_skills_total": len(resume_skills_flat),
        "sections": sections_info,
        "bullets": bullet_info,
        "has_jd": bool(jd_text and jd_text.strip())
    }

    if result["has_jd"]:
        jd_skills_by_cat = extract_skills_from_text(jd_text)
        jd_skills_flat = flatten_skills(jd_skills_by_cat)

        matched_skills = sorted(list(resume_skills_flat.intersection(jd_skills_flat)))
        missing_skills = sorted(list(jd_skills_flat.difference(resume_skills_flat)))
        extra_skills = sorted(list(resume_skills_flat.difference(jd_skills_flat)))

        # Skill match percentage
        if jd_skills_flat:
            skill_match_pct = round((len(matched_skills) / len(jd_skills_flat)) * 100)
        else:
            skill_match_pct = 75

        # Weighted keyword frequency score
        jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', jd_text.lower()))
        resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
        keyword_overlap_pct = round((len(jd_words.intersection(resume_words)) / max(1, len(jd_words))) * 100)

        # Composite ATS Score
        # 40% Skills Match, 25% Keyword Overlap, 15% Quantified Impact, 10% Action Verbs, 10% Section Completeness
        ats_score = round(
            (skill_match_pct * 0.40) +
            (keyword_overlap_pct * 0.25) +
            (bullet_info["quantification_score"] * 0.15) +
            (bullet_info["action_verb_score"] * 0.10) +
            (sections_info["section_score"] * 0.10)
        )
        ats_score = max(5, min(99, ats_score))

        result.update({
            "ats_score": ats_score,
            "skill_match_pct": skill_match_pct,
            "keyword_overlap_pct": min(100, keyword_overlap_pct * 2), # normalized
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills,
            "jd_skills_total": len(jd_skills_flat)
        })
    else:
        # General resume quality score when no JD is provided
        quality_score = round(
            (min(100, len(resume_skills_flat) * 6) * 0.35) +
            (sections_info["section_score"] * 0.25) +
            (bullet_info["quantification_score"] * 0.20) +
            (bullet_info["action_verb_score"] * 0.20)
        )
        quality_score = max(10, min(98, quality_score))
        result.update({
            "ats_score": quality_score,
            "quality_score": quality_score,
            "matched_skills": sorted(list(resume_skills_flat)),
            "missing_skills": [],
            "extra_skills": []
        })

    return result
