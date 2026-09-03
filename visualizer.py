import pandas as pd
import plotly.express as px


def create_job_match_chart(results):
    """
    Create a horizontal bar chart showing
    job-role match scores.
    """

    df = pd.DataFrame(results)

    df = df.sort_values(
        by="score",
        ascending=True
    )

    fig = px.bar(
        df,
        x="score",
        y="job_role",
        orientation="h",
        title="Job Role Match Scores",
        labels={
            "score": "Match Score (%)",
            "job_role": "Job Role",
        },
        text="score",
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
    )

    fig.update_layout(
        xaxis=dict(
            range=[0, 100]
        ),
        height=500,
    )

    return fig


def create_skill_category_chart(categorized_skills):
    """
    Create a chart showing the number of
    skills detected in each category.
    """

    data = []

    for category, skills in categorized_skills.items():

        data.append({
            "category": category.upper(),
            "count": len(skills),
        })

    df = pd.DataFrame(data)

    if df.empty:
        return None

    fig = px.pie(
        df,
        names="category",
        values="count",
        title="Skills by Category",
        hole=0.4,
    )

    return fig


def create_skill_coverage_chart(
    matched_skills,
    missing_skills,
):
    """
    Create a chart showing matched vs missing
    skills for the selected role.
    """

    data = pd.DataFrame({
        "Status": [
            "Matched Skills",
            "Missing Skills",
        ],
        "Count": [
            len(matched_skills),
            len(missing_skills),
        ],
    })

    fig = px.bar(
        data,
        x="Status",
        y="Count",
        title="Skill Coverage",
        text="Count",
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=400,
    )

    return fig