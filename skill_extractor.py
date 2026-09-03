import pandas as pd
import re


SKILL_FILE = "data/skill_dictionary.csv"


def load_skill_dictionary():
    """
    Load the controlled skill dictionary.
    """

    return pd.read_csv(SKILL_FILE)


def extract_skills(text):
    """
    Extract skills from cleaned resume text
    using skill aliases.
    """

    skill_df = load_skill_dictionary()

    found_skills = []

    text = text.lower()

    for _, row in skill_df.iterrows():

        skill = row["skill"]
        category = row["category"]
        aliases = str(row["aliases"]).split("|")

        skill_found = False

        for alias in aliases:

            alias = alias.strip().lower()

            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

            if re.search(pattern, text):
                skill_found = True
                break

        if skill_found:
            found_skills.append({
                "skill": skill,
                "category": category
            })

    return found_skills


def get_skills_by_category(found_skills):
    """
    Group extracted skills by category.
    """

    categorized = {}

    for item in found_skills:

        category = item["category"]

        if category not in categorized:
            categorized[category] = []

        categorized[category].append(item["skill"])

    return categorized