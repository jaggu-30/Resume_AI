from resume_parser import extract_resume_text


file_path = input("Enter resume path: ").strip()

with open(file_path, "rb") as file:
    text = extract_resume_text(file)

print("\n" + "=" * 60)
print("EXTRACTED RESUME TEXT")
print("=" * 60)

print(text)

print("\n" + "=" * 60)
print(f"Characters extracted: {len(text)}")
print("=" * 60)