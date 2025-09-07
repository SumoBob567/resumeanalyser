import json
from resume_parser import extract_text
from analyser import keyword_overlap, sbert_similarity

def analyze_resume_vs_job(resume_path: str, job_path: str):
    resume_text = extract_text(resume_path)

    with open(job_path, "r", encoding="utf-8") as f:
        job_text = f.read()

    overlap_results = keyword_overlap(resume_text, job_text)
    sbert_score = sbert_similarity(resume_text, job_text)

    matched_skills = sorted(overlap_results["matched"])
    missing_skills = sorted(overlap_results["missing"])

    result = {
        "sbert_score": sbert_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }

    return result


if __name__ == "__main__":
    # Example usage
    resume_file = "backend/sample_resume.docx"
    job_file = "backend/sample_job.txt"

    results = analyze_resume_vs_job(resume_file, job_file)

    # Print nicely formatted JSON
    print(json.dumps(results, indent=2))
