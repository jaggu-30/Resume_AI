from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import analyze_skill_gap


file_path = input("Enter resume path: ").strip()
target_role = input("Enter target job role: ").strip()


# Extract resume text
with open(file_path, "rb") as file:
    extracted_text = extract_resume_text(file)


# Clean resume text
cleaned_text = clean_text(extracted_text)


# Extract skills
found_skills = extract_skills(cleaned_text)

resume_skills = [
    item["skill"]
    for item in found_skills
]


# Analyze skill gap
analysis = analyze_skill_gap(
    resume_skills,
    target_role
)


print("\n" + "=" * 70)
print(f"SKILL GAP ANALYSIS — {analysis['job_role']}")
print("=" * 70)


print("\nREQUIRED SKILLS:")
for skill in analysis["required_skills"]:
    print(f"  - {skill}")


print("\nMATCHED SKILLS:")
for skill in analysis["matched_skills"]:
    print(f"  ✓ {skill}")


print("\nMISSING SKILLS:")
for skill in analysis["missing_skills"]:
    print(f"  ✗ {skill}")


print("\n" + "=" * 70)
print(
    f"Matched: {len(analysis['matched_skills'])}"
    f" / {len(analysis['required_skills'])}"
)
print("=" * 70)