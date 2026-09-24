import streamlit as st
import pandas as pd
import re

from navigation import top_navigation

from resume_section_analyzer import extract_resume_sections
from report_generator import generate_pdf_report
from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills, get_skills_by_category
from job_matcher import (
    calculate_match_scores,
    analyze_skill_gap,
)
from roadmap_generator import generate_roadmap
from visualizer import (
    create_job_match_chart,
    create_skill_category_chart,
    create_skill_coverage_chart,
)
from learning_resources import (
    get_resources_for_skill,
    get_resources_for_skills,
    get_youtube_search_url,
)

# ---- NEW: ATS & Quality modules (additive, non-destructive) ----
from ats_analyzer import analyze_ats
from resume_quality_analyzer import analyze_resume_quality, analyze_ai_writing

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)


top_navigation("resume")
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HELPER FOR CUSTOM HTML
# ============================================================

def render_html(html):
    """
    Render custom HTML correctly in Streamlit.
    Removes leading indentation from every line.
    """
    html = "\n".join(
        line.strip()
        for line in html.strip().splitlines()
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )

# ============================================================
# CUSTOM CSS
# ============================================================

render_html(
    """
<style>

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    padding: 2.5rem 2.5rem;
    border-radius: 26px;
    margin-bottom: 2rem;

    background:
        linear-gradient(
            135deg,
            rgba(79, 70, 229, 0.18),
            rgba(37, 99, 235, 0.12),
            rgba(16, 185, 129, 0.10)
        );

    border: 1px solid rgba(148, 163, 184, 0.20);
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.8rem;
}

.hero-subtitle {
    font-size: 1.08rem;
    line-height: 1.7;
    opacity: 0.75;
    max-width: 850px;
}


/* =========================================================
   SECTION HEADERS
   ========================================================= */

.section-title {
    font-size: 1.85rem;
    font-weight: 800;
    margin-top: 2.4rem;
    margin-bottom: 0.4rem;
}

.section-description {
    opacity: 0.65;
    margin-bottom: 1.3rem;
}


/* =========================================================
   GENERAL CARDS
   ========================================================= */

.card {
    padding: 1.4rem;
    border-radius: 20px;

    background: rgba(128, 128, 128, 0.055);

    border: 1px solid rgba(148, 163, 184, 0.17);

    margin-bottom: 1rem;
}


/* =========================================================
   CAREER MATCH CARDS
   ========================================================= */

.match-card {
    padding: 1.4rem;
    border-radius: 20px;

    background: rgba(128, 128, 128, 0.055);

    border: 1px solid rgba(148, 163, 184, 0.18);

    min-height: 205px;
}

.match-rank {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    opacity: 0.6;
    margin-bottom: 0.5rem;
}

.match-role {
    font-size: 1.3rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
}

.match-score {
    font-size: 2rem;
    font-weight: 850;
    margin-bottom: 0.5rem;
}

.match-description {
    font-size: 0.88rem;
    line-height: 1.5;
    opacity: 0.65;
}


/* =========================================================
   SKILL PILLS
   ========================================================= */

.skill-pill {
    display: inline-block;

    padding: 0.45rem 0.85rem;
    margin: 0.25rem;

    border-radius: 999px;

    background: rgba(99, 102, 241, 0.10);

    border: 1px solid rgba(99, 102, 241, 0.22);

    font-size: 0.88rem;
    font-weight: 600;
}

.matched-pill {
    display: inline-block;

    padding: 0.45rem 0.85rem;
    margin: 0.25rem;

    border-radius: 999px;

    background: rgba(34, 197, 94, 0.10);

    border: 1px solid rgba(34, 197, 94, 0.25);

    font-size: 0.88rem;
    font-weight: 600;
}

.missing-pill {
    display: inline-block;

    padding: 0.45rem 0.85rem;
    margin: 0.25rem;

    border-radius: 999px;

    background: rgba(239, 68, 68, 0.10);

    border: 1px solid rgba(239, 68, 68, 0.25);

    font-size: 0.88rem;
    font-weight: 600;
}


/* =========================================================
   ROADMAP
   ========================================================= */

.roadmap-card {
    padding: 1.2rem 1.4rem;

    border-left: 4px solid rgba(99, 102, 241, 0.7);

    border-radius: 0 16px 16px 0;

    background: rgba(128, 128, 128, 0.055);

    margin-bottom: 0.9rem;
}

.week-label {
    font-size: 0.75rem;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    opacity: 0.6;
}

.roadmap-skill {
    font-size: 1.2rem;
    font-weight: 800;
    margin: 0.25rem 0;
}


/* =========================================================
   RESOURCE CARDS
   ========================================================= */

.resource-card {
    padding: 1.15rem;

    border-radius: 18px;

    background: rgba(128, 128, 128, 0.045);

    border: 1px solid rgba(148, 163, 184, 0.17);

    min-height: 170px;
}

.resource-type {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    opacity: 0.55;
}

.resource-title {
    font-size: 1rem;
    font-weight: 750;
    margin-top: 0.45rem;
}

.resource-provider {
    font-size: 0.82rem;
    opacity: 0.65;
    margin-top: 0.25rem;
}

.resource-level {
    font-size: 0.8rem;
    margin-top: 0.6rem;
    opacity: 0.7;
}

.free-badge {
    display: inline-block;

    margin-top: 0.55rem;

    padding: 0.25rem 0.55rem;

    border-radius: 999px;

    background: rgba(34, 197, 94, 0.12);

    border: 1px solid rgba(34, 197, 94, 0.25);

    font-size: 0.72rem;

    font-weight: 700;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    margin-top: 4rem;
    padding-top: 1.5rem;

    border-top: 1px solid rgba(148, 163, 184, 0.17);

    text-align: center;

    opacity: 0.5;

    font-size: 0.82rem;
}

</style>
"""
)


# ============================================================
# HERO
# ============================================================

render_html(
    """
<div class="hero">
    <div class="hero-title">
        🤖 AI Resume Analyzer
    </div>

    <div class="hero-subtitle">
        Understand your resume, discover your best career matches,
        identify missing skills, and get a personalized learning path.
    </div>
</div>
"""
)


# ============================================================
# RESPONSIBLE AI
# ============================================================

with st.expander(
    "🛡️ Responsible AI Notice",
    expanded=False,
):

    st.info(
        """
        This application provides career guidance based on
        job-related information from your resume.

        Match scores are estimates and should not be treated
        as hiring, rejection, or employment decisions.

        The system focuses on skills, education, projects,
        certifications, and experience.

        It does not intentionally evaluate candidates using
        sensitive attributes such as gender, age, religion,
        nationality, photograph, marital status, or disability.

        A missing keyword does not necessarily mean that the
        candidate lacks the underlying ability.
        """
    )


# ============================================================
# UPLOAD
# ============================================================

render_html(
    """
<div class="section-title">
    📄 Upload Your Resume
</div>

<div class="section-description">
    Upload a PDF or DOCX resume to start your personalized analysis.
</div>
"""
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX",
)


if uploaded_file is None:

    st.info(
        "👆 Upload your resume above to generate your personalized analysis."
    )

    render_html(
        """
<div class="card">

<h3>🔍 What the analyzer does</h3>

<p><strong>1. Extract</strong> → Reads your resume content</p>

<p><strong>2. Clean</strong> → Normalizes extracted text</p>

<p><strong>3. Analyze</strong> → Detects skills and resume sections</p>

<p><strong>4. Match</strong> → Compares your skills with job roles</p>

<p><strong>5. Identify gaps</strong> → Finds missing skills</p>

<p><strong>6. Recommend</strong> → Creates a learning roadmap</p>

<p><strong>7. Learn</strong> → Provides courses, videos and practice resources</p>

</div>
"""
    )

    st.stop()


# ============================================================
# RESUME EXTRACTION
# ============================================================

st.success(
    f"✅ Uploaded: {uploaded_file.name}"
)


try:

    extracted_text = extract_resume_text(
        uploaded_file
    )

except Exception as error:

    st.error(
        f"❌ Error while reading the resume: {error}"
    )

    st.stop()


if not extracted_text.strip():

    st.error(
        "❌ No readable text was found in the resume."
    )

    st.stop()


# ============================================================
# TEXT CLEANING
# ============================================================

cleaned_text = clean_text(
    extracted_text
)


# ============================================================
# SKILL EXTRACTION
# ============================================================

found_skills = extract_skills(
    cleaned_text
)

resume_skills = [
    item["skill"]
    for item in found_skills
]

categorized_skills = get_skills_by_category(
    found_skills
)


if not resume_skills:

    st.warning(
        "⚠️ No recognized technical skills were detected."
    )

    with st.expander(
        "📜 View Extracted Text"
    ):

        st.text_area(
            "Resume text",
            extracted_text,
            height=350,
        )

    st.stop()


# ============================================================
# RESUME SECTION ANALYSIS
# ============================================================

sections = extract_resume_sections(
    extracted_text
)


# ============================================================
# JOB MATCHING
# ============================================================

results = calculate_match_scores(
    resume_skills
)

top_roles = results[:3]


# ============================================================
# SNAPSHOT
# ============================================================

render_html(
    """
<div class="section-title">
    📊 Resume Snapshot
</div>

<div class="section-description">
    A quick overview of your resume analysis.
</div>
"""
)

best_role = (
    results[0]["job_role"]
    if results
    else "N/A"
)

best_score = (
    results[0]["score"]
    if results
    else 0
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "Skills Detected",
        len(resume_skills),
    )

with metric2:

    st.metric(
        "Best Career Match",
        best_role,
    )

with metric3:

    st.metric(
        "Best Match",
        f"{best_score:.1f}%",
    )

with metric4:

    st.metric(
        "Resume Sections",
        len(sections),
    )


# ============================================================
# DETECTED SKILLS
# ============================================================

render_html(
    """
<div class="section-title">
    🧠 Detected Skills
</div>

<div class="section-description">
    Technical skills identified from your resume.
</div>
"""
)

skill_html = ""

for skill in resume_skills:

    skill_html += (
        f'<span class="skill-pill">⚡ {skill}</span>'
    )

render_html(
    skill_html
)


# ============================================================
# SKILL DISTRIBUTION
# ============================================================

render_html(
    """
<div class="section-title">
    📚 Skill Distribution
</div>
"""
)

chart_col1, chart_col2 = st.columns(
    [1.3, 1]
)

with chart_col1:

    skill_chart = create_skill_category_chart(
        categorized_skills
    )

    if skill_chart is not None:

        st.plotly_chart(
            skill_chart,
            width="stretch",
        )

with chart_col2:

    for category, skills in categorized_skills.items():

        st.markdown(
            f"### {category.upper()}"
        )

        st.write(
            ", ".join(skills)
        )


# ============================================================
# RESUME SECTION ANALYSIS
# ============================================================

render_html(
    """
<div class="section-title">
    📋 Resume Section Analysis
</div>

<div class="section-description">
    Important sections detected from your resume.
</div>
"""
)

section_titles = {
    "education": "🎓 Education",
    "projects": "💻 Projects",
    "experience": "💼 Experience / Internships",
    "certifications": "📜 Certifications",
    "skills": "🛠️ Skills",
}

if sections:

    for section_name, content in sections.items():

        title = section_titles.get(
            section_name,
            section_name.title(),
        )

        with st.expander(
            title,
            expanded=True,
        ):

            if content.strip():

                clean_content = re.sub(
                    r"[•●▪◦]",
                    "\n",
                    content,
                )

                lines = clean_content.splitlines()

                for line in lines:

                    line = line.strip()

                    if line:

                        st.write(
                            f"• {line}"
                        )

            else:

                st.info(
                    "No information found in this section."
                )

else:

    st.warning(
        "No standard resume sections were detected."
    )


# ============================================================
# CAREER MATCH
# ============================================================

render_html(
    """
<div class="section-title">
    🎯 Career Match
</div>

<div class="section-description">
    See which job roles best match your current skill profile.
</div>
"""
)

medals = [
    "🥇",
    "🥈",
    "🥉",
]

match_columns = st.columns(
    min(3, len(top_roles))
)

for index, role in enumerate(top_roles):

    with match_columns[index]:

        render_html(
            f"""
<div class="match-card">

    <div class="match-rank">
        {medals[index]} TOP MATCH
    </div>

    <div class="match-role">
        {role["job_role"]}
    </div>

    <div class="match-score">
        {role["score"]:.1f}%
    </div>

    <div class="match-description">
        {role["description"]}
    </div>

</div>
"""
        )


# ============================================================
# ALL ROLE SCORES
# ============================================================

st.markdown(
    "### 📊 All Job Role Scores"
)

results_df = pd.DataFrame(
    [
        {
            "Job Role": item["job_role"],
            "Match Score (%)": item["score"],
            "Skill Score (%)": item["skill_score"],
            "TF-IDF Similarity (%)": item["tfidf_score"],
        }
        for item in results
    ]
)

st.dataframe(
    results_df,
    width="stretch",
    hide_index=True,
)


job_chart = create_job_match_chart(
    results
)

st.plotly_chart(
    job_chart,
    width="stretch",
)


# ============================================================
# TARGET ROLE
# ============================================================

render_html(
    """
<div class="section-title">
    🎯 Choose Your Target Role
</div>

<div class="section-description">
    Select the career you want to prepare for.
</div>
"""
)

available_roles = [
    result["job_role"]
    for result in results
]

score_lookup = {
    result["job_role"]: result["score"]
    for result in results
}


def role_label(role):

    return (
        f"{role} "
        f"— {score_lookup.get(role, 0):.1f}% match"
    )


target_role = st.selectbox(
    "Target job role",
    available_roles,
    format_func=role_label,
)


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

analysis = analyze_skill_gap(
    resume_skills,
    target_role,
)

matched_skills = analysis[
    "matched_skills"
]

missing_skills = analysis[
    "missing_skills"
]

required_skills = analysis[
    "required_skills"
]


render_html(
    f"""
<div class="section-title">
    📉 Skill Gap Analysis
</div>

<div class="section-description">
    Your current skills compared with the requirements for
    <strong>{target_role}</strong>.
</div>
"""
)


gap1, gap2, gap3 = st.columns(3)

with gap1:

    st.metric(
        "Required Skills",
        len(required_skills),
    )

with gap2:

    st.metric(
        "Matched Skills",
        len(matched_skills),
    )

with gap3:

    st.metric(
        "Missing Skills",
        len(missing_skills),
    )


if required_skills:

    coverage = (
        len(matched_skills)
        / len(required_skills)
    )

else:

    coverage = 0


st.progress(
    coverage,
    text=f"{coverage * 100:.1f}% skill coverage",
)


matched_col, missing_col = st.columns(2)


with matched_col:

    st.markdown(
        "### 🟢 Matched Skills"
    )

    if matched_skills:

        matched_html = ""

        for skill in matched_skills:

            matched_html += (
                f'<span class="matched-pill">✓ {skill}</span>'
            )

        render_html(
            matched_html
        )

    else:

        st.info(
            "No required skills matched yet."
        )


with missing_col:

    st.markdown(
        "### 🔴 Missing Skills"
    )

    if missing_skills:

        missing_html = ""

        for skill in missing_skills:

            missing_html += (
                f'<span class="missing-pill">✕ {skill}</span>'
            )

        render_html(
            missing_html
        )

    else:

        st.success(
            "🎉 You match all required skills!"
        )


coverage_chart = create_skill_coverage_chart(
    matched_skills,
    missing_skills,
)

st.plotly_chart(
    coverage_chart,
    width="stretch",
)


# ============================================================
# LEARNING ROADMAP
# ============================================================

roadmap = generate_roadmap(
    missing_skills
)


render_html(
    """
<div class="section-title">
    🗺️ Personalized Learning Roadmap
</div>

<div class="section-description">
    Follow this sequence to work on the skills required
    for your selected career.
</div>
"""
)


if roadmap:

    for item in roadmap:

        render_html(
            f"""
<div class="roadmap-card">

    <div class="week-label">
        WEEK {item["week"]}
    </div>

    <div class="roadmap-skill">
        📚 {item["skill"]}
    </div>

    <div>
        {item["topic"]}
    </div>

</div>
"""
        )

else:

    st.success(
        "🎉 No learning gaps identified for this role."
    )


# ============================================================
# LEARNING HUB
# ============================================================

render_html(
    """
<div class="section-title">
    🚀 Learning Hub
</div>

<div class="section-description">
    Curated learning resources for the skills you need to improve.
    Explore courses, videos, documentation, and practice platforms.
</div>
"""
)


if missing_skills:

    st.info(
        f"📚 {len(missing_skills)} skill(s) need attention. "
        "Start with the roadmap above."
    )

    for week_number, skill in enumerate(
        missing_skills,
        start=1,
    ):

        resources = get_resources_for_skill(
            skill
        )

        with st.expander(
            f"🔴 Week {week_number} — Learn {skill}",
            expanded=(week_number == 1),
        ):

            if resources:

                # Show maximum 3 curated resources
                selected_resources = resources[:3]

                resource_columns = st.columns(
                    len(selected_resources)
                )

                for index, resource in enumerate(
                    selected_resources
                ):

                    with resource_columns[index]:

                        resource_type = resource.get(
                            "type",
                            "Resource",
                        )

                        title = resource.get(
                            "title",
                            "Learning Resource",
                        )

                        provider = resource.get(
                            "provider",
                            "",
                        )

                        url = resource.get(
                            "url",
                            "#",
                        )

                        level = resource.get(
                            "level",
                            "All Levels",
                        )

                        is_free = (
                            str(
                                resource.get(
                                    "is_free",
                                    "",
                                )
                            ).lower()
                            == "yes"
                        )

                        free_badge = (
                            '<div class="free-badge">🆓 FREE</div>'
                            if is_free
                            else ""
                        )

                        render_html(
                            f"""
<div class="resource-card">

    <div class="resource-type">
        {resource_type}
    </div>

    <div class="resource-title">
        {title}
    </div>

    <div class="resource-provider">
        {provider}
    </div>

    <div class="resource-level">
        🎯 {level}
    </div>

    {free_badge}

</div>
"""
                        )

                        st.markdown(
                            f"[🔗 Open Resource]({url})"
                        )

            else:

                st.warning(
                    "No curated resources are available yet."
                )

                youtube_url = (
                    get_youtube_search_url(
                        skill
                    )
                )

                st.markdown(
                    f"[🎥 Find {skill} tutorials on YouTube]({youtube_url})"
                )

            st.markdown(
                "### 💡 How to learn this skill"
            )

            st.write(
                f"""
                Start with a beginner-friendly resource for
                **{skill}**, practice what you learn, and then
                build a small project using the skill.
                """
            )

            st.markdown(
                "### 🏗️ Suggested Project"
            )

            st.write(
                f"Build a small practical project using **{skill}** "
                "and add it to your GitHub portfolio."
            )

else:

    st.success(
        "🎉 No missing skills — your current profile covers this role."
    )


# ============================================================
# ADDITIONAL SUGGESTIONS
# ============================================================

render_html(
    """
<div class="section-title">
    💡 Improve Your Resume Further
</div>

<div class="section-description">
    Learning the skill is only half the job. Show evidence of it.
</div>
"""
)


suggestion1, suggestion2, suggestion3 = st.columns(3)


with suggestion1:

    render_html(
        """
<div class="card">

<h3>🏗️ Build Projects</h3>

<p>
Create practical projects using your missing skills.
Real projects give you evidence to discuss during interviews.
</p>

</div>
"""
    )


with suggestion2:

    render_html(
        """
<div class="card">

<h3>🐙 Use GitHub</h3>

<p>
Publish your projects, document what you built,
and keep your repositories organized.
</p>

</div>
"""
    )


with suggestion3:

    render_html(
        """
<div class="card">

<h3>🔄 Re-analyze</h3>

<p>
After learning new skills, update your resume and
run the analyzer again to see how your career matches change.
</p>

</div>
"""
    )


# ============================================================
# ATS & RESUME QUALITY  (NEW — additive section)
# ============================================================

render_html(
    """
<div class="section-title">
    📊 ATS &amp; Resume Quality
</div>

<div class="section-description">
    Estimated ATS compatibility, keyword coverage, resume quality review,
    and AI-writing originality indicators for your selected target role.
</div>
"""
)

try:

    ats_results = analyze_ats(
        extracted_text=extracted_text,
        resume_skills=resume_skills,
        sections=sections,
        target_role=target_role,
    )

    quality_results = analyze_resume_quality(extracted_text)
    ai_results      = analyze_ai_writing(extracted_text)

    # ----------------------------------------------------------
    # ATS SCORE — big hero metric
    # ----------------------------------------------------------

    render_html(
        """
<div class="card" style="margin-bottom:1.5rem;">
<p style="font-size:0.8rem;font-weight:700;letter-spacing:1px;
           text-transform:uppercase;opacity:0.55;margin-bottom:0.4rem;">
    Estimated ATS Compatibility Score
</p>
"""
    )

    ats_score = ats_results["ats_score"]

    if ats_score >= 75:
        score_color = "#22c55e"
        score_label = "Good"
    elif ats_score >= 50:
        score_color = "#f59e0b"
        score_label = "Moderate"
    else:
        score_color = "#ef4444"
        score_label = "Needs Improvement"

    render_html(
        f"""
<p style="font-size:3.2rem;font-weight:900;color:{score_color};
           margin:0;line-height:1;">
    {ats_score} <span style="font-size:1.4rem;opacity:0.6;">/ 100</span>
</p>
<p style="font-size:0.9rem;color:{score_color};margin-top:0.3rem;">
    {score_label}
</p>
</div>
"""
    )

    # ----------------------------------------------------------
    # BREAKDOWN METRICS
    # ----------------------------------------------------------

    breakdown = ats_results["breakdown"]

    st.markdown("#### 📈 Score Breakdown")

    col_a, col_b, col_c = st.columns(3)

    breakdown_items = list(breakdown.items())

    with col_a:
        label, val = breakdown_items[0]   # Keyword Coverage
        st.metric(label, f"{val:.0f}%")
        st.progress(min(val / 100, 1.0))

    with col_b:
        label, val = breakdown_items[1]   # Skill Coverage
        st.metric(label, f"{val:.0f}%")
        st.progress(min(val / 100, 1.0))

    with col_c:
        label, val = breakdown_items[2]   # Section Completeness
        st.metric(label, f"{val:.0f}%")
        st.progress(min(val / 100, 1.0))

    col_d, col_e, _ = st.columns(3)

    with col_d:
        label, val = breakdown_items[3]   # Resume Structure
        st.metric(label, f"{val:.0f}%")
        st.progress(min(val / 100, 1.0))

    with col_e:
        label, val = breakdown_items[4]   # Contact Info
        st.metric(label, f"{val:.0f}%")
        st.progress(min(val / 100, 1.0))

    # ----------------------------------------------------------
    # KEYWORD MATCH
    # ----------------------------------------------------------

    st.markdown("---")
    kw_col_a, kw_col_b = st.columns(2)

    with kw_col_a:
        st.markdown("##### ✅ Matched Keywords")
        matched_kws = ats_results["keyword_cov"]["matched"]
        if matched_kws:
            matched_kw_html = ""
            for kw in matched_kws:
                matched_kw_html += (
                    f'<span class="matched-pill">✓ {kw}</span>'
                )
            render_html(matched_kw_html)
        else:
            st.info("No required keywords matched for this role.")

    with kw_col_b:
        st.markdown("##### ❌ Missing Important Keywords")
        missing_kws = ats_results["keyword_cov"]["missing"]
        if missing_kws:
            missing_kw_html = ""
            for kw in missing_kws:
                missing_kw_html += (
                    f'<span class="missing-pill">✗ {kw}</span>'
                )
            render_html(missing_kw_html)
        else:
            st.success("🎉 All required keywords are present!")

    # ----------------------------------------------------------
    # ATS IMPROVEMENT SUGGESTIONS
    # ----------------------------------------------------------

    with st.expander(
        "💡 ATS Improvement Suggestions",
        expanded=False,
    ):
        for suggestion in ats_results["suggestions"]:
            st.markdown(f"• {suggestion}")

    # ----------------------------------------------------------
    # RESUME QUALITY REVIEW
    # ----------------------------------------------------------

    st.markdown("---")
    st.markdown("#### 📝 Resume Quality Review")

    ql = quality_results["quality_levels"]

    q1, q2, q3 = st.columns(3)
    with q1:
        st.metric("Generic Phrases", quality_results["generic_count"])
    with q2:
        st.metric("Repeated Phrases",
                  len(quality_results["repeated_phrases"]))
    with q3:
        st.metric("Quantified Achievements",
                  quality_results["quantified_count"])

    render_html(
        """
<div class="card" style="margin-top:0.8rem;">
"""
    )

    for metric_name, level in ql.items():
        if level == "Low":
            icon = "🔴"
        elif level == "Moderate":
            icon = "🟡"
        else:
            icon = "🟢"
        st.markdown(
            f"**{metric_name}** — {icon} {level}"
        )

    render_html("</div>")

    with st.expander(
        "📋 Quality Improvement Suggestions",
        expanded=False,
    ):
        for s in quality_results["suggestions"]:
            st.markdown(f"• {s}")

        if quality_results["generic_phrases"]:
            st.markdown("**Generic phrases detected:**")
            for gp in quality_results["generic_phrases"][:5]:
                st.markdown(f"  - *{gp}*")

        if quality_results["buzzwords_found"]:
            st.markdown("**Buzzwords found:**")
            for bw in quality_results["buzzwords_found"][:5]:
                st.markdown(f"  - *{bw}*")

    # ----------------------------------------------------------
    # AI-WRITING / ORIGINALITY REVIEW
    # ----------------------------------------------------------

    st.markdown("---")
    st.markdown("#### 🔍 AI-Writing / Originality Review")

    render_html(
        """
<div style="font-size:0.78rem;opacity:0.55;margin-bottom:1rem;">
⚠️ These are qualitative pattern indicators only.
This system cannot determine whether content is AI-generated,
and does not produce an AI-generation percentage.
Use these suggestions to make your resume more specific and authentic.
</div>
"""
    )

    ai_ind = ai_results["indicators"]

    ai_col1, ai_col2 = st.columns(2)

    ind_items = list(ai_ind.items())
    half = (len(ind_items) + 1) // 2

    with ai_col1:
        for metric_name, level in ind_items[:half]:
            if metric_name in ("Quantified Achievements",
                               "Specificity", "Action-Oriented Language"):
                # For these, High is GOOD
                icon = "🟢" if level == "High" else ("🟡" if level == "Moderate" else "🔴")
            else:
                # For these, Low is GOOD
                icon = "🟢" if level == "Low" else ("🟡" if level == "Moderate" else "🔴")
            st.markdown(f"**{metric_name}** — {icon} {level}")

    with ai_col2:
        for metric_name, level in ind_items[half:]:
            if metric_name in ("Quantified Achievements",
                               "Specificity", "Action-Oriented Language",
                               "Sentence Variety"):
                icon = "🟢" if level in ("High", "Low") else "🟡"
            else:
                icon = "🟢" if level == "Low" else ("🟡" if level == "Moderate" else "🔴")
            st.markdown(f"**{metric_name}** — {icon} {level}")

    with st.expander(
        "💬 Originality Suggestions",
        expanded=False,
    ):
        for s in ai_results["suggestions"]:
            st.markdown(f"• {s}")

except Exception as ats_error:

    st.warning(
        f"⚠️ ATS analysis could not complete: {ats_error}. "
        "Your existing resume analysis above is unaffected."
    )


# ============================================================
# PDF REPORT
# ============================================================

render_html(
    """
<div class="section-title">
    📄 Download Analysis Report
</div>

<div class="section-description">
    Generate a PDF containing your resume analysis,
    career recommendations, skill gaps, and roadmap.
</div>
"""
)


try:

    report_data = generate_pdf_report(
        resume_name=uploaded_file.name,
        resume_skills=found_skills,
        recommendations=top_roles,
        target_role=target_role,
        skill_analysis=analysis,
        roadmap=roadmap,
        ats_results=locals().get("ats_results"),
        quality_results=locals().get("quality_results"),
    )

    st.download_button(
        label="📥 Download PDF Report",
        data=report_data,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf",
    )

except Exception as error:

    st.error(
        f"❌ Unable to generate PDF report: {error}"
    )


# ============================================================
# EXTRACTED TEXT
# ============================================================

render_html(
    """
<div class="section-title">
    📜 Extracted Resume Text
</div>

<div class="section-description">
    View the raw text extracted from your uploaded resume.
</div>
"""
)


with st.expander(
    "View Extracted Resume Text"
):

    st.text_area(
        "Resume Text",
        extracted_text,
        height=400,
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
<div class="footer">

    🤖 <strong>AI Resume Analyzer</strong>
    &nbsp;•&nbsp;
    Career guidance based on job-related resume information

    <br><br>

    ⚠️ Match scores are estimates and should not be used
    as hiring or rejection decisions.

</div>
"""
)