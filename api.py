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
    allow_origins=["*"],  # you can restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_text: str = Form(...)
):
    # Save uploaded resume temporarily
    suffix = os.path.splitext(resume.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(resume.file, tmp)
        tmp_path = tmp.name

    try:
        # Extract text from resume (PDF or DOCX)
        resume_text = extract_text(tmp_path)

        # Run analysis
        sbert_score = sbert_similarity(resume_text, job_text)
        overlap_results = keyword_overlap(resume_text, job_text)

        result = {
            "sbert_score": sbert_score,
            "matched_skills": sorted(overlap_results["matched"]),
            "missing_skills": sorted(overlap_results["missing"])
        }

        return JSONResponse(content=result)

    finally:
        # Cleanup temp file
        os.remove(tmp_path)
