from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import calculate_match_scores, get_top_roles


file_path = input("Enter resume path: ").strip()


# 1. Extract resume text
with open(file_path, "rb") as file:
    extracted_text = extract_resume_text(file)


# 2. Clean resume text
cleaned_text = clean_text(extracted_text)


# 3. Extract skills
found_skills = extract_skills(cleaned_text)

resume_skills = [
    item["skill"]
    for item in found_skills
]


# 4. Calculate job-role scores
results = calculate_match_scores(resume_skills)


print("\n" + "=" * 70)
print("JOB ROLE MATCHING RESULTS")
print("=" * 70)


for rank, result in enumerate(results, start=1):

    print(
        f"{rank}. {result['job_role']}"
        f" - {result['score']}%"
    )


# 5. Display top 3
top_roles = get_top_roles(resume_skills)


print("\n" + "=" * 70)
print("TOP 3 RECOMMENDED ROLES")
print("=" * 70)


for rank, result in enumerate(top_roles, start=1):

    print(
        f"{rank}. {result['job_role']}"
        f" - {result['score']}%"
    )

    print(f"   {result['description']}")