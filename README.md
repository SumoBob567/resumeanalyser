# Resume Analyzer

A full-stack web application that analyzes resumes against a job description to provide semantic and keyword-based match scores. Built using **FastAPI** for the backend, **React** for the frontend, and **Sentence Transformers (SBERT)** for natural language understanding.

---

## Table of Contents
- [Demo](#demo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)

---

## Demo
You can access the deployed application here:
**Backend no longer deployed due to RAM requirements exceeding 512MB (Render's Free Tier)**

- **Frontend:** [Vercel URL](https://resumeanalyser-olive.vercel.app)
- **Backend:** [Render URL](https://resumeanalyser-lrlz.onrender.com)

---

## Features
- **Semantic Match Score:** Uses SBERT embeddings to calculate similarity between resume content and job description.
- **Keyword Matching:** Identifies which job-required skills are present or missing in a resume.
- **Importance Classification:** Tags skills as high, medium, or low importance based on contextual cues in the job description.
- **File Upload Support:** Accepts PDF, DOCX, and TXT resume files.
- **REST API:** Fully functional backend API with `/analyze` endpoint.
- **CORS-enabled:** Allows secure communication between frontend and backend.

---

## Tech Stack
- **Frontend:** React, Tailwind CSS
- **Backend:** FastAPI, Python 3.13
- **NLP & ML:** `sentence-transformers`, `scikit-learn`
- **Deployment:** 
  - Frontend: Vercel  
  - Backend: Render  
- **Data Processing:** `python-docx`, `PyMuPDF`, `regex`, `tempfile`

---

## Installation

### Backend
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/resume-analyzer.git
   cd resume-analyzer

2. Create and activate a virtual environment:
    python -m venv .venv
    source .venv/bin/activate   # Linux/Mac
    .venv\Scripts\activate      # Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Start the backend server:
    uvicorn api:app --host 0.0.0.0 --port 10000

5. Access API documentation at http://localhost:8000/docs

### Frontend

Run the following from the project root:
 - cd frontend
 - npm install
 - npm start


## Usage

 - Upload a resume (PDF/DOCX)
 - Enter a job description
 - Click Analyze
 - Receive:
   - Semantic match score (0-100%)
   - Matched skills
   - Missing skills