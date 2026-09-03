from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf_report(
    resume_name,
    resume_skills,
    recommendations,
    target_role,
    skill_analysis,
    roadmap,
):
    """
    Generate a downloadable PDF analysis report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
    )

    normal_style = styles["BodyText"]

    story = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "AI Resume Analysis Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Resume:</b> {resume_name}",
            normal_style,
        )
    )

    story.append(Spacer(1, 15))

    # --------------------------------------------------
    # DETECTED SKILLS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "1. Detected Skills",
            heading_style,
        )
    )

    if resume_skills:

        skill_data = [
            ["Skill", "Category"]
        ]

        for item in resume_skills:
            skill_data.append(
                [
                    item["skill"],
                    item["category"],
                ]
            )

        table = Table(
            skill_data,
            colWidths=[250, 150],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                ]
            )
        )

        story.append(table)

    else:

        story.append(
            Paragraph(
                "No skills detected.",
                normal_style,
            )
        )

    # --------------------------------------------------
    # RECOMMENDED ROLES
    # --------------------------------------------------

    story.append(
        Paragraph(
            "2. Recommended Job Roles",
            heading_style,
        )
    )

    role_data = [
        ["Rank", "Job Role", "Match Score"]
    ]

    for index, role in enumerate(
        recommendations,
        start=1,
    ):

        role_data.append(
            [
                str(index),
                role["job_role"],
                f"{role['score']}%",
            ]
        )

    table = Table(
        role_data,
        colWidths=[60, 250, 100],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
            ]
        )
    )

    story.append(table)

    # --------------------------------------------------
    # TARGET ROLE
    # --------------------------------------------------

    story.append(
        Paragraph(
            f"3. Target Role: {target_role}",
            heading_style,
        )
    )

    matched = skill_analysis[
        "matched_skills"
    ]

    missing = skill_analysis[
        "missing_skills"
    ]

    story.append(
        Paragraph(
            "<b>Matched Skills</b>",
            normal_style,
        )
    )

    if matched:

        for skill in matched:

            story.append(
                Paragraph(
                    f"✓ {skill}",
                    normal_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "No matching skills found.",
                normal_style,
            )
        )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            normal_style,
        )
    )

    if missing:

        for skill in missing:

            story.append(
                Paragraph(
                    f"✗ {skill}",
                    normal_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "No missing skills identified.",
                normal_style,
            )
        )

    # --------------------------------------------------
    # LEARNING ROADMAP
    # --------------------------------------------------

    story.append(
        Paragraph(
            "4. Learning Roadmap",
            heading_style,
        )
    )

    if roadmap:

        roadmap_data = [
            ["Week", "Skill", "Learning Topic"]
        ]

        for item in roadmap:

            roadmap_data.append(
                [
                    f"Week {item['week']}",
                    item["skill"],
                    item["topic"],
                ]
            )

        table = Table(
            roadmap_data,
            colWidths=[70, 100, 240],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                ]
            )
        )

        story.append(table)

    else:

        story.append(
            Paragraph(
                "No learning gaps identified.",
                normal_style,
            )
        )

    # --------------------------------------------------
    # RESPONSIBLE AI NOTE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "5. Responsible AI Notice",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "This report provides educational guidance based "
            "on job-related resume information. Match scores "
            "are estimates and should not be treated as "
            "automatic hiring or rejection decisions.",
            normal_style,
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()