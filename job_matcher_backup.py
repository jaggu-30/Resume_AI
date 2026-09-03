import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


JOB_ROLE_FILE = "data/job_roles.csv"


def load_job_roles():
    """
    Load job roles and their required skills.
    """
    return pd.read_csv(JOB_ROLE_FILE)


def get_required_skills(job_role):
    """
    Get the required skills for a specific job role.
    """

    job_roles = load_job_roles()

    role = job_roles[
        job_roles["job_role"].str.lower() == job_role.lower()
    ]

    if role.empty:
        return []

    skills = role.iloc[0]["skills"]

    return [
        skill.strip()
        for skill in str(skills).split("|")
        if skill.strip()
    ]


def calculate_match_scores(resume_skills):
    """
    Compare resume skills with all job roles
    using TF-IDF and cosine similarity.
    """

    job_roles = load_job_roles()

    resume_text = " ".join(resume_skills)

    job_texts = job_roles["skills"].fillna("").tolist()

    documents = [resume_text] + job_texts

    vectorizer = TfidfVectorizer(
        lowercase=True,
        token_pattern=r"(?u)\b[\w+#.-]+\b"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    results = []

    for index, score in enumerate(similarities):

        results.append({
            "job_role": job_roles.iloc[index]["job_role"],
            "score": round(float(score) * 100, 2),
            "description": job_roles.iloc[index]["description"]
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


def get_top_roles(resume_skills, top_n=3):
    """
    Return the top N recommended job roles.
    """

    results = calculate_match_scores(resume_skills)

    return results[:top_n]


def analyze_skill_gap(resume_skills, job_role):
    """
    Compare resume skills with the required skills
    for a selected job role.
    """

    required_skills = get_required_skills(job_role)

    resume_skills_lower = {
        skill.lower().strip()
        for skill in resume_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower().strip() in resume_skills_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "job_role": job_role,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }