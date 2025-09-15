from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import tempfile
import shutil
import os
import time

from backend.resume_parser import extract_text
from backend.analyser import keyword_overlap, sbert_similarity, get_model

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_model()
    yield

app = FastAPI(title="Resume Analyzer API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}

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
        if os.path.getsize(tmp_path) == 0:
            return JSONResponse(
            status_code=400,
            content={"error": "Uploaded file is empty"}
            )
        
        start = time.time()
        resume_text = extract_text(tmp_path)
        print("Extract text:", time.time() - start, "s")

        start = time.time()
        sbert_score = sbert_similarity(resume_text, job_text)
        print("Extract text:", time.time() - start, "s")

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

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    finally:
        os.remove(tmp_path)
