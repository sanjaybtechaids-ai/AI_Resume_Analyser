from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.concurrency import run_in_threadpool

from analyzer.ai_client import generate_ai_critique
from analyzer.nlp_engine import analyze_resume_vs_jd, calculate_originality
from analyzer.parser import extract_text_from_bytes
from analyzer.templates import PRESET_JOB_DESCRIPTIONS

app = FastAPI(title="ResumeIQ", docs_url=None, redoc_url=None)
MAX_REQUEST_BYTES = 4_000_000
MAX_FILE_BYTES = 2_000_000
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
INDEX_FILE = Path(__file__).parent / "static" / "index.html"


@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length:
        if not content_length.isdecimal():
            return JSONResponse(status_code=400, content={"detail": "Invalid request size."})
        if int(content_length) > MAX_REQUEST_BYTES:
            return JSONResponse(
                status_code=413,
                content={"detail": "The complete request must be smaller than 4 MB."},
            )
    return await call_next(request)


@app.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    return HTMLResponse(INDEX_FILE.read_text(encoding="utf-8"))


@app.get("/api/templates")
async def job_description_templates() -> dict:
    return PRESET_JOB_DESCRIPTIONS


async def _extract_upload(upload: Optional[UploadFile], label: str) -> str:
    if upload is None:
        return ""

    extension = Path(upload.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail=f"{label} must be a PDF, DOCX, or TXT file.")

    data = await upload.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail=f"{label} file must be 2 MB or smaller.")

    text, _ = extract_text_from_bytes(data, upload.filename or "")
    if text.startswith("Error parsing "):
        raise HTTPException(status_code=422, detail=text)
    return text


def _build_report(analysis: dict, originality: dict, feedback: dict) -> str:
    lines = [
        "# ResumeIQ Analysis Report",
        "",
        "## Summary",
        f"- ATS match: {analysis['ats_score']}%",
        f"- Skills match: {analysis.get('skill_match_pct', 'N/A')}%",
        f"- Quantified impact: {analysis['bullets']['quantification_score']}%",
        f"- Action strength: {analysis['bullets']['action_verb_score']}%",
        f"- Originality estimate: {originality['originality_score']}%",
        f"- Similarity estimate: {originality['similarity_score']}%",
        "",
        "## Recruiter verdict",
        feedback.get("executive_summary", ""),
        "",
        "## Matched skills",
        ", ".join(analysis.get("matched_skills", [])) or "None",
        "",
        "## Missing skills",
        ", ".join(analysis.get("missing_skills", [])) or "None",
        "",
        "## Bullet rewrites",
    ]
    for index, rewrite in enumerate(feedback.get("bullet_rewrites", []), 1):
        lines.extend(
            [
                "",
                f"### Revision {index}",
                f"- Before: {rewrite['original']}",
                f"- Recommended: {rewrite['revised']}",
                f"- Why: {rewrite['rationale']}",
            ]
        )
    return "\n".join(lines)


@app.post("/api/analyze")
async def analyze(
    resume_file: Optional[UploadFile] = File(default=None),
    resume_text: str = Form(default=""),
    jd_text: str = Form(default=""),
    reference_file: Optional[UploadFile] = File(default=None),
    reference_text: str = Form(default=""),
    provider: str = Form(default="auto"),
    api_key: str = Form(default=""),
) -> dict:
    if provider not in {"auto", "gemini", "openai"}:
        raise HTTPException(status_code=422, detail="Choose a supported analysis engine.")
    if len(api_key) > 500:
        raise HTTPException(status_code=422, detail="The API key is too long.")
    if len(resume_text) > 1_000_000 or len(reference_text) > 1_000_000 or len(jd_text) > 1_000_000:
        raise HTTPException(status_code=413, detail="Each text field must be smaller than 1 MB.")

    uploaded_resume = await _extract_upload(resume_file, "Resume")
    source_resume = uploaded_resume if resume_file is not None else resume_text
    if len(source_resume.strip()) < 40:
        raise HTTPException(status_code=400, detail="Provide a resume with at least 40 characters.")

    uploaded_reference = await _extract_upload(reference_file, "Reference")
    source_reference = uploaded_reference if reference_file is not None else reference_text

    analysis = await run_in_threadpool(analyze_resume_vs_jd, source_resume, jd_text)
    originality = await run_in_threadpool(calculate_originality, source_resume, source_reference)
    feedback = await run_in_threadpool(
        generate_ai_critique,
        source_resume,
        jd_text,
        analysis,
        api_key.strip() or None,
        provider,
    )

    return {
        "analysis": analysis,
        "originality": originality,
        "feedback": feedback,
        "report_markdown": _build_report(analysis, originality, feedback),
    }
