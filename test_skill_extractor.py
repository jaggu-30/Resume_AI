from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills, get_skills_by_category


file_path = input("Enter resume path: ").strip()


# Extract resume text
with open(file_path, "rb") as file:
    extracted_text = extract_resume_text(file)


# Clean resume text
cleaned_text = clean_text(extracted_text)


# Extract skills
found_skills = extract_skills(cleaned_text)


# Group skills by category
categorized_skills = get_skills_by_category(found_skills)


print("\n" + "=" * 60)
print("SKILLS DETECTED")
print("=" * 60)


for category, skills in categorized_skills.items():

    print(f"\n{category.upper()}:")

    for skill in skills:
        print(f"  - {skill}")


print("\n" + "=" * 60)
print(f"TOTAL SKILLS FOUND: {len(found_skills)}")
print("=" * 60)