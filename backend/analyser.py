import re
from collections import Counter
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_skills(file_path="backend/skills.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

SKILL_KEYWORDS = load_skills()


def clean_and_tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+]', ' ', text)  # keep alphanumeric
    tokens = [t for t in text.split() if t not in ENGLISH_STOP_WORDS]
    return tokens

def extract_keywords(text: str, top_n=20):
    tokens = clean_and_tokenize(text)
    counts = Counter(tokens)
    return [word for word, freq in counts.most_common(top_n)]

def keyword_overlap(resume_text: str, job_text: str):
    resume_text_lower = resume_text.lower()
    job_text_lower = job_text.lower()

    matched = []
    missing = []

    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        in_resume = re.search(pattern, resume_text_lower)
        in_job = re.search(pattern, job_text_lower)

        if in_job:
            if in_resume:
                matched.append(skill)
            else:
                missing.append(skill)

    match_score = round(len(matched) / max(len(matched) + len(missing), 1) * 100, 2)

    return {
        "matched": sorted(set(matched)),
        "missing": sorted(set(missing)),
        "match_score": match_score
    }



def tfidf_similarity(resume_text: str, job_text: str) -> float:
    documents = [resume_text, job_text]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(similarity[0][0]) * 100, 2)

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def sbert_similarity(resume_text: str, job_text: str) -> float:
    embeddings = sbert_model.encode([resume_text, job_text])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    return round(float(similarity[0][0]) * 100, 2)

if __name__ == "__main__":

    resume_text = "Python developer with experience in machine learning and SQL databases."
    job_text = " We are looking for a software engineer skilled in Python, SQL, cloud computing, and data analysis. Experience with machine learning is a plus."

    results = keyword_overlap(resume_text, job_text)
    print("Matched Skills:", results["matched"])
    print("Missing Skills:", results["missing"])
    print("Keyword Overlap Match Score:", results["match_score"], "%")

    tfidf_score = tfidf_similarity(resume_text, job_text)
    print("TF-IDF Match Score:", tfidf_score, "%")

    score = sbert_similarity(resume_text, job_text)
    print("Sentence-BERT Semantic Similarity Score:", score, "%")
