from roadmap_generator import generate_roadmap


missing_skills = [
    "SQL",
    "Pandas",
    "Power BI",
    "Docker"
]


roadmap = generate_roadmap(missing_skills)


print("\n" + "=" * 70)
print("LEARNING ROADMAP")
print("=" * 70)


for item in roadmap:

    print(
        f"\nWeek {item['week']}: {item['skill']}"
    )

    print(
        f"  Topic: {item['topic']}"
    )


print("\n" + "=" * 70)