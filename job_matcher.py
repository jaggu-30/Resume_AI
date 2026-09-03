import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

JOB_ROLE_FILE = "data/job_roles.csv"


def load_job_roles():
    return pd.read_csv(JOB_ROLE_FILE)


def get_required_skills(job_role):
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


def calculate_skill_overlap(resume_skills, required_skills):
    resume_set = {
        skill.lower().strip()
        for skill in resume_skills
    }

    required_set = {
        skill.lower().strip()
        for skill in required_skills
    }

    if not required_set:
        return 0.0

    matched = resume_set.intersection(required_set)

    return (len(matched) / len(required_set)) * 100


def calculate_tfidf_similarity(resume_skills, required_skills):
    resume_text = " ".join(resume_skills)
    role_text = " ".join(required_skills)

    documents = [resume_text, role_text]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        token_pattern=r"(?u)\b[\w+#.-]+\b"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return float(similarity) * 100


def calculate_hybrid_score(resume_skills, required_skills):
    skill_score = calculate_skill_overlap(
        resume_skills,
        required_skills
    )

    tfidf_score = calculate_tfidf_similarity(
        resume_skills,
        required_skills
    )

    final_score = (
        skill_score * 0.70
        + tfidf_score * 0.30
    )

    return round(final_score, 2)


def calculate_match_scores(resume_skills):
    job_roles = load_job_roles()

    if not resume_skills:
        return []

    # ---------------------------------------------------------
    # Prepare job-role skill lists
    # ---------------------------------------------------------
    role_data = []

    for _, row in job_roles.iterrows():

        required_skills = [
            skill.strip()
            for skill in str(row["skills"]).split("|")
            if skill.strip()
        ]

        role_data.append({
            "job_role": row["job_role"],
            "required_skills": required_skills,
            "description": row["description"]
        })

    # ---------------------------------------------------------
    # Calculate all TF-IDF similarities together
    # ---------------------------------------------------------
    resume_text = " ".join(resume_skills)

    documents = [resume_text]

    for role in role_data:
        documents.append(
            " ".join(role["required_skills"])
        )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        token_pattern=r"(?u)\b[\w+#.-]+\b"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    # ---------------------------------------------------------
    # Calculate final hybrid scores
    # ---------------------------------------------------------
    results = []

    for index, role in enumerate(role_data):

        required_skills = role["required_skills"]

        skill_score = calculate_skill_overlap(
            resume_skills,
            required_skills
        )

        tfidf_score = float(similarity_scores[index]) * 100

        final_score = (
            skill_score * 0.70
            + tfidf_score * 0.30
        )

        results.append({
            "job_role": role["job_role"],
            "score": round(final_score, 2),
            "skill_score": round(skill_score, 2),
            "tfidf_score": round(tfidf_score, 2),
            "description": role["description"]
        })

    # Highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


def get_top_roles(resume_skills, top_n=3):
    results = calculate_match_scores(resume_skills)

    return results[:top_n]


def analyze_skill_gap(resume_skills, job_role):
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