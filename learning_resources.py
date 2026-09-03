import pandas as pd
from functools import lru_cache
from urllib.parse import quote_plus


RESOURCE_FILE = "data/learning_resources.csv"


@lru_cache(maxsize=1)
def load_learning_resources():
    """
    Load the learning resource dataset.

    The CSV is cached so it is not repeatedly
    loaded during the application runtime.
    """
    return pd.read_csv(RESOURCE_FILE).fillna("")


def get_resource_for_skill(skill):
    """
    Return all learning resources available for one skill.
    """

    resources = load_learning_resources()

    skill_name = str(skill).strip().lower()

    matched = resources[
        resources["skill"]
        .astype(str)
        .str.strip()
        .str.lower()
        == skill_name
    ]

    if matched.empty:
        return []

    return matched.to_dict("records")


def get_resources_for_skill(skill):
    """
    Alias for get_resource_for_skill().

    This provides a clearer plural-style function name
    for use in the Streamlit application.
    """
    return get_resource_for_skill(skill)


def get_resources_for_skills(skills):
    """
    Return resources grouped by skill.

    Example:

    {
        "SQL": [
            {...},
            {...}
        ],
        "Pandas": [
            {...}
        ]
    }
    """

    result = {}

    for skill in skills:
        resources = get_resource_for_skill(skill)

        if resources:
            result[skill] = resources

    return result


def get_resources_by_type(skill):
    """
    Organize resources for one skill by resource type.

    Example:

    {
        "Course": [...],
        "Practice": [...],
        "Video": [...]
    }
    """

    resources = get_resource_for_skill(skill)

    grouped = {}

    for resource in resources:
        resource_type = resource.get("type", "Other")

        if resource_type not in grouped:
            grouped[resource_type] = []

        grouped[resource_type].append(resource)

    return grouped


def get_youtube_search_url(skill):
    """
    Generate a YouTube search URL for a skill.

    Used as a fallback when a curated video
    is not available in the dataset.
    """

    query = quote_plus(
        f"{skill} tutorial for beginners"
    )

    return (
        "https://www.youtube.com/results?search_query="
        + query
    )


def get_resource_summary(skill):
    """
    Return a summary of available resources.
    """

    resources = get_resource_for_skill(skill)

    if not resources:
        return {
            "skill": skill,
            "total": 0,
            "free": 0,
            "types": []
        }

    free_count = sum(
        1
        for resource in resources
        if str(
            resource.get("is_free", "")
        ).lower() == "yes"
    )

    resource_types = sorted(
        {
            resource.get("type", "Other")
            for resource in resources
        }
    )

    return {
        "skill": skill,
        "total": len(resources),
        "free": free_count,
        "types": resource_types
    }