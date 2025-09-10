from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile
import shutil
import os

from backend.resume_parser import extract_text
from backend.analyser import keyword_overlap, sbert_similarity

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Resume Analyzer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_text: str = Form(...)
):
    suffix = os.path.splitext(resume.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(resume.file, tmp)
        tmp_path = tmp.name

    try:
        resume_text = extract_text(tmp_path)

        sbert_score = sbert_similarity(resume_text, job_text)
        overlap_results = keyword_overlap(resume_text, job_text)

        matched_skills = overlap_results["matched"]
        missing_skills = overlap_results["missing"]

        total_skills = len(matched_skills) + len(missing_skills)
        match_ratio = len(matched_skills) / total_skills if total_skills > 0 else 0

        final_score = round((sbert_score * 0.65) + (match_ratio * 100 * 0.35), 2)

        result = {
            "final_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }

        return JSONResponse(content=result)

    finally:
        os.remove(tmp_path)
