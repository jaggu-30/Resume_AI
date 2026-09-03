from resume_parser import extract_resume_text
from text_cleaner import clean_text


file_path = input("Enter resume path: ").strip()

with open(file_path, "rb") as file:
    extracted_text = extract_resume_text(file)

cleaned_text = clean_text(extracted_text)

print("\n" + "=" * 60)
print("CLEANED RESUME TEXT")
print("=" * 60)

print(cleaned_text)

print("\n" + "=" * 60)
print(f"Original characters: {len(extracted_text)}")
print(f"Cleaned characters:  {len(cleaned_text)}")
print("=" * 60)