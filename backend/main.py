import json
from resume_parser import extract_text
from analyser import keyword_overlap, sbert_similarity

def analyse_resume_vs_job(resume_path: str, job_path: str):
    resume_text = extract_text(resume_path)

    with open(job_path, "r", encoding="utf-8") as f:
        job_text = f.read()

    overlap_results = keyword_overlap(resume_text, job_text)
    sbert_score = sbert_similarity(resume_text, job_text)

    matched_skills = overlap_results["matched"]
    missing_skills = overlap_results["missing"]

    total_skills = len(matched_skills) + len(missing_skills)
    match_ratio = len(matched_skills) / total_skills if total_skills > 0 else 0

    final_score = round((sbert_score * 0.75) + (match_ratio * 100 * 0.25), 2)

    result = {
        "final_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }

    return result


if __name__ == "__main__":
    resume_file = "backend/sample_resume.docx"
    job_file = "backend/sample_job.txt"
    results = analyse_resume_vs_job(resume_file, job_file)
    print(json.dumps(results, indent=2))
