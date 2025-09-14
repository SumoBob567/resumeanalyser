import re
from collections import Counter
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_skills(file_path="backend/skills.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

SKILL_KEYWORDS = load_skills()
SKILL_LIST = sorted(list(SKILL_KEYWORDS))
#SKILL_EMBEDDINGS = sbert_model.encode(SKILL_LIST, convert_to_tensor=True)

sbert_model = None
SKILL_EMBEDDINGS = None

def get_model():
    global sbert_model, SKILL_EMBEDDINGS
    if sbert_model is None:
        sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
        SKILL_EMBEDDINGS = sbert_model.encode(SKILL_LIST, convert_to_tensor=True)
        example_embeddings = {
            level: sbert_model.encode(examples, convert_to_tensor=True)
            for level, examples in importance_examples.items()
        }

    return sbert_model, SKILL_EMBEDDINGS, example_embeddings

def clean_and_tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+]', ' ', text)  # keep alphanumeric
    tokens = [t for t in text.split() if t not in ENGLISH_STOP_WORDS]
    return tokens

def extract_keywords(text: str, top_n=20):
    tokens = clean_and_tokenize(text)
    counts = Counter(tokens)
    return [word for word, freq in counts.most_common(top_n)]

def _chunk_text_for_embedding(text: str):
    chunks = re.split(r'[,\n.;?!]', text)
    return [c.strip() for c in chunks if c.strip()]

def keyword_overlap(resume_text: str, job_text: str, job_threshold: float = 0.60, resume_threshold: float = 0.60):
    sbert_model, SKILL_EMBEDDINGS, example_embeddings = get_model()
    resume_text_lower = resume_text.lower()
    job_text_lower = job_text.lower()

    matched = []
    missing = []

    resume_chunks = _chunk_text_for_embedding(resume_text_lower)
    job_chunks = _chunk_text_for_embedding(job_text_lower)

    if not resume_chunks:
        resume_chunks = [resume_text_lower] if resume_text_lower.strip() else []
    if not job_chunks:
        job_chunks = [job_text_lower] if job_text_lower.strip() else []

    resume_chunk_emb = None
    job_chunk_emb = None
    if resume_chunks:
        resume_chunk_emb = sbert_model.encode(resume_chunks, convert_to_tensor=True)
    if job_chunks:
        job_chunk_emb = sbert_model.encode(job_chunks, convert_to_tensor=True)

    for i, skill in enumerate(SKILL_LIST):
        pattern = r"\b" + re.escape(skill) + r"\b"

        exact_in_job = bool(re.search(pattern, job_text_lower))
        exact_in_resume = bool(re.search(pattern, resume_text_lower))

        in_job = exact_in_job
        if not in_job and job_chunk_emb is not None:
            skill_emb = SKILL_EMBEDDINGS[i : i+1]
            sims = util.cos_sim(skill_emb, job_chunk_emb)
            max_sim = float(sims.max().item())
            if max_sim >= job_threshold:
                in_job = True

        if not in_job:
            continue

        importance = classify_importance(skill, job_text)

        in_resume = exact_in_resume
        if not in_resume and resume_chunk_emb is not None:
            skill_emb = SKILL_EMBEDDINGS[i : i+1]
            sims = util.cos_sim(skill_emb, resume_chunk_emb)
            max_sim = float(sims.max().item())
            if max_sim >= resume_threshold:
                in_resume = True

        if in_resume:
            matched.append({"skill": skill, "importance": importance})
        else:
            missing.append({"skill": skill, "importance": importance})

    return {"matched": matched, "missing": missing}

def sbert_similarity(resume_text: str, job_text: str) -> float:
    sbert_model, SKILL_EMBEDDINGS, example_embeddings = get_model()
    embeddings = sbert_model.encode([resume_text, job_text])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    return round(float(similarity[0][0]) * 100, 2)

importance_examples = {
    "high": [
        "X is required",
        "X is a must-have",
        "mandatory knowledge of X",
        "strong proficiency in X is essential"
    ],
    "medium": [
        "X is preferred",
        "X would be helpful",
        "experience with X is a plus",
        "familiarity with X is good to have"
    ],
    "low": [
        "X is optional",
        "nice to have experience with X",
        "bonus if you know X",
        "basic knowledge of X is acceptable"
    ]
}

"""example_embeddings = {
    level: sbert_model.encode(examples, convert_to_tensor=True)
    for level, examples in importance_examples.items()
}"""

def classify_importance(skill: str, job_text: str) -> str:
    sbert_model, SKILL_EMBEDDINGS, example_embeddings = get_model()
    sentences = re.split(r'[.!\n]', job_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    pattern = r"\b" + re.escape(skill.lower()) + r"\b"
    relevant_sentences = [s for s in sentences if re.search(pattern, s.lower())]

    if not relevant_sentences:
        return "low"

    best_level = "medium"
    best_score = -1

    for sentence in relevant_sentences:
        sent_embedding = sbert_model.encode(sentence, convert_to_tensor=True)
        for level, ex_embeddings in example_embeddings.items():
            score = util.cos_sim(sent_embedding, ex_embeddings).max().item()
            if score > best_score:
                best_score = score
                best_level = level

    return best_level
