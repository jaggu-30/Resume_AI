from resume_parser import extract_resume_text
from resume_section_analyzer import extract_resume_sections


file_path = input("Enter resume path: ").strip()


with open(file_path, "rb") as file:

    resume_text = extract_resume_text(file)


sections = extract_resume_sections(
    resume_text
)


print("\n" + "=" * 70)
print("RESUME SECTION ANALYSIS")
print("=" * 70)


for section, content in sections.items():

    print(
        f"\n[{section.upper()}]"
    )

    print(content)


print("\n" + "=" * 70)
print(
    f"Sections detected: {len(sections)}"
)
print("=" * 70)