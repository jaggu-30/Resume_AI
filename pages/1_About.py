import streamlit as st
from pathlib import Path
import base64
from navigation import top_navigation

top_navigation("about")

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="About | AI Resume Analyzer",
    page_icon="👨‍💻",
    layout="wide",
)


# ============================================================
# HTML RENDER HELPER
# ============================================================

def render_html(html):
    html = "\n".join(
        line.strip()
        for line in html.strip().splitlines()
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# FIND PROFILE PHOTO
# ============================================================

PAGE_DIR = Path(__file__).parent

photo_candidates = [
    PAGE_DIR / "profile.jpg",
    PAGE_DIR / "profile.jpeg",
    PAGE_DIR / "profile.png",
]

profile_photo = None

for photo in photo_candidates:
    if photo.exists():
        profile_photo = photo
        break


def image_to_base64(image_path):

    if image_path is None:
        return None

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()


profile_image = image_to_base64(profile_photo)


# ============================================================
# CSS
# ============================================================

render_html(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ============================================================
   ANIMATIONS
   ============================================================ */

@keyframes fadeUp {

    from {
        opacity: 0;
        transform: translateY(25px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


@keyframes fadeLeft {

    from {
        opacity: 0;
        transform: translateX(-30px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }

}


@keyframes gradientFlow {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }

}


@keyframes photoGlow {

    0% {
        box-shadow:
            0 0 15px rgba(59, 130, 246, 0.20);
    }

    50% {
        box-shadow:
            0 0 35px rgba(59, 130, 246, 0.45);
    }

    100% {
        box-shadow:
            0 0 15px rgba(59, 130, 246, 0.20);
    }

}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    position: relative;

    overflow: hidden;

    padding: 2rem 2.2rem;

    border-radius: 24px;

    background:
        linear-gradient(
            120deg,
            #182334,
            #1d3143,
            #162b35
        );

    background-size: 250% 250%;

    border:
        1px solid
        rgba(148, 163, 184, 0.20);

    animation:
        fadeUp 0.8s ease-out,
        gradientFlow 12s ease infinite;

    margin-bottom: 1rem;
}


.hero-content {

    display: flex;

    align-items: center;

    gap: 2.4rem;
}


/* ============================================================
   SQUARE PROFILE PHOTO
   ============================================================ */

.photo-frame {

    width: 175px;

    height: 175px;

    flex-shrink: 0;

    padding: 4px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #3b82f6,
            #06b6d4,
            #8b5cf6,
            #3b82f6
        );

    background-size: 300% 300%;

    animation:
        gradientFlow 7s ease infinite,
        photoGlow 3s ease-in-out infinite;
}


.profile-photo {

    width: 100%;

    height: 100%;

    display: block;

    object-fit: cover;

    border-radius: 13px;

    border:
        4px solid
        #101827;
}


/* ============================================================
   HERO TEXT
   ============================================================ */

.hero-text {
    flex: 1;
}


.eyebrow {

    font-size: 0.72rem;

    font-weight: 800;

    letter-spacing: 2px;

    opacity: 0.55;

    margin-bottom: 0.5rem;
}


.name {

    font-size: 3rem;

    font-weight: 900;

    line-height: 1.05;

    margin-bottom: 0.65rem;
}


.role {

    font-size: 1.05rem;

    font-weight: 700;

    line-height: 1.45;

    opacity: 0.82;

    margin-bottom: 0.65rem;
}


.tagline {

    max-width: 700px;

    font-size: 0.9rem;

    line-height: 1.6;

    opacity: 0.62;
}


/* ============================================================
   BADGES
   ============================================================ */

.badges {

    display: flex;

    flex-wrap: wrap;

    gap: 0.45rem;

    margin-top: 1rem;
}


.badge {

    padding:
        0.4rem
        0.7rem;

    border-radius: 999px;

    background:
        rgba(255, 255, 255, 0.055);

    border:
        1px solid
        rgba(255, 255, 255, 0.12);

    font-size: 0.75rem;

    font-weight: 700;

    transition:
        transform 0.25s ease,
        background 0.25s ease;
}


.badge:hover {

    transform: translateY(-3px);

    background:
        rgba(255, 255, 255, 0.10);
}


/* ============================================================
   STATS
   ============================================================ */

.stats {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 0.7rem;

    margin-top: 1.5rem;
}


.stat {

    padding: 0.75rem;

    border-radius: 15px;

    text-align: center;

    background:
        rgba(255, 255, 255, 0.045);

    border:
        1px solid
        rgba(255, 255, 255, 0.10);

    transition:
        transform 0.25s ease,
        background 0.25s ease;
}


.stat:hover {

    transform: translateY(-4px);

    background:
        rgba(255, 255, 255, 0.08);
}


.stat-number {

    font-size: 1.35rem;

    font-weight: 900;
}


.stat-label {

    font-size: 0.65rem;

    font-weight: 700;

    opacity: 0.48;

    margin-top: 0.15rem;
}


/* ============================================================
   SECTION
   ============================================================ */

.section {

    margin-top: 2.8rem;

    animation:
        fadeUp 0.7s ease-out;
}


.section-heading {

    font-size: 1.75rem;

    font-weight: 850;

    margin-bottom: 0.25rem;
}


.section-subtitle {

    font-size: 0.85rem;

    opacity: 0.52;

    margin-bottom: 1.2rem;
}


/* ============================================================
   ABOUT CARDS
   ============================================================ */

.about-card {

    padding: 1.35rem;

    min-height: 190px;

    border-radius: 19px;

    background:
        rgba(128, 128, 128, 0.045);

    border:
        1px solid
        rgba(148, 163, 184, 0.15);

    transition:
        transform 0.3s ease,
        border-color 0.3s ease,
        box-shadow 0.3s ease;
}


.about-card:hover {

    transform: translateY(-6px);

    border-color:
        rgba(59, 130, 246, 0.38);

    box-shadow:
        0 15px 35px
        rgba(0, 0, 0, 0.15);
}


.about-card h3 {

    margin-top: 0;

    font-size: 1.1rem;
}


.about-card p {

    font-size: 0.88rem;

    line-height: 1.65;

    opacity: 0.68;
}


/* ============================================================
   CURRENTLY BUILDING
   ============================================================ */

.build-card {

    padding: 1.35rem;

    min-height: 150px;

    border-radius: 19px;

    background:
        linear-gradient(
            135deg,
            rgba(59, 130, 246, 0.09),
            rgba(16, 185, 129, 0.06)
        );

    border:
        1px solid
        rgba(59, 130, 246, 0.18);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease;
}


.build-card:hover {

    transform: translateY(-6px);

    box-shadow:
        0 15px 30px
        rgba(0, 0, 0, 0.14);
}


.build-title {

    font-size: 1.1rem;

    font-weight: 850;

    margin-bottom: 0.5rem;
}


.build-description {

    font-size: 0.84rem;

    line-height: 1.6;

    opacity: 0.62;
}


/* ============================================================
   PROJECTS
   ============================================================ */

.project-card {

    padding: 1.25rem;

    min-height: 165px;

    border-radius: 18px;

    background:
        rgba(128, 128, 128, 0.045);

    border:
        1px solid
        rgba(148, 163, 184, 0.15);

    transition:
        transform 0.3s ease,
        border-color 0.3s ease,
        box-shadow 0.3s ease;

    margin-bottom: 1rem;
}


.project-card:hover {

    transform: translateY(-7px);

    border-color:
        rgba(99, 102, 241, 0.40);

    box-shadow:
        0 15px 35px
        rgba(0, 0, 0, 0.15);
}


.project-number {

    font-size: 0.62rem;

    font-weight: 850;

    letter-spacing: 1.5px;

    opacity: 0.38;
}


.project-title {

    font-size: 1rem;

    font-weight: 850;

    margin-top: 0.4rem;

    margin-bottom: 0.5rem;
}


.project-description {

    font-size: 0.8rem;

    line-height: 1.55;

    opacity: 0.62;
}


/* ============================================================
   SKILLS
   ============================================================ */

.skill-group {

    padding: 1.15rem;

    border-radius: 18px;

    background:
        rgba(128, 128, 128, 0.045);

    border:
        1px solid
        rgba(148, 163, 184, 0.14);

    margin-bottom: 0.75rem;
}


.skill-group-title {

    font-size: 0.92rem;

    font-weight: 800;

    margin-bottom: 0.7rem;
}


.skill-pills {

    display: flex;

    flex-wrap: wrap;

    gap: 0.4rem;
}


.skill-pill {

    padding:
        0.38rem
        0.65rem;

    border-radius: 999px;

    font-size: 0.73rem;

    font-weight: 650;

    background:
        rgba(99, 102, 241, 0.08);

    border:
        1px solid
        rgba(99, 102, 241, 0.18);

    transition:
        transform 0.2s ease,
        background 0.2s ease;
}


.skill-pill:hover {

    transform: translateY(-3px);

    background:
        rgba(99, 102, 241, 0.15);
}


/* ============================================================
   EDUCATION / EXPERIENCE
   ============================================================ */

.info-panel {

    padding: 1.35rem;

    border-radius: 19px;

    background:
        rgba(128, 128, 128, 0.045);

    border:
        1px solid
        rgba(148, 163, 184, 0.15);

    min-height: 150px;

    transition:
        transform 0.3s ease,
        border-color 0.3s ease;
}


.info-panel:hover {

    transform: translateY(-5px);

    border-color:
        rgba(59, 130, 246, 0.35);
}


.info-title {

    font-size: 1.05rem;

    font-weight: 850;

    margin-bottom: 0.45rem;
}


.info-company {

    font-size: 0.85rem;

    opacity: 0.55;

    margin-bottom: 0.8rem;
}


.info-text {

    font-size: 0.82rem;

    line-height: 1.6;

    opacity: 0.64;
}


/* ============================================================
   CERTIFICATIONS
   ============================================================ */

.certification {

    padding:
        0.9rem
        1.1rem;

    border-radius: 14px;

    background:
        rgba(128, 128, 128, 0.045);

    border:
        1px solid
        rgba(148, 163, 184, 0.14);

    margin-bottom: 0.55rem;

    font-size: 0.83rem;

    transition:
        transform 0.25s ease,
        border-color 0.25s ease;
}


.certification:hover {

    transform: translateX(6px);

    border-color:
        rgba(99, 102, 241, 0.35);
}


/* ============================================================
   FINAL CARD
   ============================================================ */

.final-card {

    margin-top: 2.5rem;

    padding: 2rem;

    border-radius: 22px;

    text-align: center;

    background:
        linear-gradient(
            135deg,
            rgba(59, 130, 246, 0.08),
            rgba(16, 185, 129, 0.07)
        );

    border:
        1px solid
        rgba(148, 163, 184, 0.16);
}


.final-title {

    font-size: 1.45rem;

    font-weight: 850;

    margin-bottom: 0.6rem;
}


.final-text {

    max-width: 750px;

    margin: auto;

    font-size: 0.88rem;

    line-height: 1.7;

    opacity: 0.62;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    margin-top: 3.5rem;

    padding-top: 1.3rem;

    border-top:
        1px solid
        rgba(148, 163, 184, 0.13);

    text-align: center;

    font-size: 0.75rem;

    opacity: 0.42;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .hero-content {

        flex-direction: column;

        text-align: center;

    }

    .badges {

        justify-content: center;

    }

    .name {

        font-size: 2.35rem;

    }

    .stats {

        grid-template-columns:
            repeat(2, 1fr);

    }

}

</style>
"""
)


# ============================================================
# PROFILE PHOTO HTML
# ============================================================

if profile_image:

    extension = profile_photo.suffix.lower()

    if extension == ".png":

        mime_type = "image/png"

    else:

        mime_type = "image/jpeg"


    photo_html = f"""
<div class="photo-frame">

<img
    class="profile-photo"
    src="data:{mime_type};base64,{profile_image}"
    alt="Jagadeesh Nayak V">

</div>
"""

else:

    photo_html = """
<div class="photo-frame">

<div
style="
width:100%;
height:100%;
border-radius:13px;
display:flex;
align-items:center;
justify-content:center;
background:#172033;
font-size:4rem;
"
>
👨‍💻
</div>

</div>
"""


# ============================================================
# HERO
# ============================================================

render_html(
    f"""
<div class="hero">

<div class="hero-content">

{photo_html}

<div class="hero-text">

<div class="eyebrow">
AI • MACHINE LEARNING • SOFTWARE
</div>

<div class="name">
Jagadeesh Nayak V
</div>

<div class="role">
B.E. Computer Science & Engineering
— Artificial Intelligence & Machine Learning
</div>

<div class="tagline">
I build practical AI-powered applications,
automation systems, and software projects while
continuously exploring modern AI and machine
learning technologies.
</div>

<div class="badges">

<span class="badge">
🤖 AI / ML
</span>

<span class="badge">
🐍 Python
</span>

<span class="badge">
⚙️ Backend
</span>

<span class="badge">
🚀 Automation
</span>

</div>

</div>

</div>


<div class="stats">

<div class="stat">
<div class="stat-number">6</div>
<div class="stat-label">PROJECTS</div>
</div>

<div class="stat">
<div class="stat-number">7.9</div>
<div class="stat-label">CGPA</div>
</div>

<div class="stat">
<div class="stat-number">2027</div>
<div class="stat-label">GRADUATION</div>
</div>

<div class="stat">
<div class="stat-number">1</div>
<div class="stat-label">AI INTERNSHIP</div>
</div>

</div>

</div>
"""
)


# ============================================================
# ABOUT ME
# ============================================================

render_html(
    """
<div class="section">

<div class="section-heading">
👋 About Me
</div>

<div class="section-subtitle">
A little about what drives me.
</div>

</div>
"""
)


about_col1, about_col2 = st.columns(2)


with about_col1:

    render_html(
        """
<div class="about-card">

<h3>
🧠 Who I Am
</h3>

<p>
I am an engineering student specializing in
Artificial Intelligence and Machine Learning,
with a strong interest in building practical
software and AI-powered applications.
</p>

<p>
I enjoy turning ideas into working systems
and learning through real-world projects.
</p>

</div>
"""
    )


with about_col2:

    render_html(
        """
<div class="about-card">

<h3>
⚡ What I Focus On
</h3>

<p>
My interests include Artificial Intelligence,
Machine Learning, backend development,
automation, APIs, data processing, and
modern AI technologies.
</p>

<p>
My goal is to continuously improve through
projects, experimentation, and learning.
</p>

</div>
"""
    )


# ============================================================
# CURRENTLY BUILDING
# ============================================================

render_html(
    """
<div class="section">

<div class="section-heading">
🔥 Currently Building
</div>

<div class="section-subtitle">
Projects I am actively working on.
</div>

</div>
"""
)


build_col1, build_col2 = st.columns(2)


with build_col1:

    render_html(
        """
<div class="build-card">

<div class="build-title">
🤖 Jarvis
</div>

<div class="build-description">
A personal AI laptop assistant designed to
understand commands, interact with the computer,
and automate useful tasks.
</div>

</div>
"""
    )


with build_col2:

    render_html(
        """
<div class="build-card">

<div class="build-title">
📄 AI Resume Analyzer
</div>

<div class="build-description">
An NLP-based system that analyzes resumes,
matches skills with career roles, identifies
skill gaps, and recommends personalized
learning resources.
</div>

</div>
"""
    )


# ============================================================
# PROJECTS
# ============================================================

render_html(
    """
<div class="section">

<div class="section-heading">
🚀 Projects
</div>

<div class="section-subtitle">
Selected technical projects.
</div>

</div>
"""
)


projects = [

    (
        "01",
        "🤖 Jarvis",
        "Personal AI laptop assistant for automation, computer interaction, and task execution."
    ),

    (
        "02",
        "⚡ Automated Smart Energy Meter",
        "IoT-based energy monitoring system designed to measure and present electricity consumption."
    ),

    (
        "03",
        "👁️ Vision Based Aerowriting",
        "Computer-vision project exploring gesture-based interaction through visual input."
    ),

    (
        "04",
        "🔐 Behavioral Biometric Security System",
        "Security-focused project exploring behavioral patterns for biometric identification."
    ),

    (
        "05",
        "🧠 AI Repo-Mind",
        "AI-focused project designed around understanding and working with software repositories."
    ),

    (
        "06",
        "📄 AI Resume Analyzer",
        "NLP-based career analysis system providing role matching, skill-gap analysis, roadmap generation, and learning resources."
    ),

]


project_columns = st.columns(3)


for index, project in enumerate(projects):

    number, title, description = project

    with project_columns[index % 3]:

        render_html(
            f"""
<div class="project-card">

<div class="project-number">
PROJECT {number}
</div>

<div class="project-title">
{title}
</div>

<div class="project-description">
{description}
</div>

</div>
"""
        )


# ============================================================
# TECHNICAL SKILLS
# ============================================================

render_html(
    """
<div class="section">

<div class="section-heading">
🛠️ Technical Skills
</div>

<div class="section-subtitle">
Technologies and tools I work with.
</div>

</div>
"""
)


skill_groups = {

    "🤖 AI & Machine Learning": [

        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "PyTorch",
        "Scikit-learn",
        "LLM",
        "RAG",
        "OpenCV",

    ],

    "🐍 Programming & Data": [

        "Python",
        "Java",
        "C",
        "SQL",
        "Pandas",
        "NumPy",
        "Excel",
        "Power BI",

    ],

    "⚙️ Backend & APIs": [

        "FastAPI",
        "Django",
        "Flask",
        "REST API",
        "MySQL",

    ],

    "🚀 Tools & Platforms": [

        "Git",
        "GitHub",
        "Docker",
        "Canva",
        "MS Word",
        "MS PowerPoint",

    ],

}


for group_name, group_skills in skill_groups.items():

    skills_html = f"""
<div class="skill-group">

<div class="skill-group-title">
{group_name}
</div>

<div class="skill-pills">
"""


    for skill in group_skills:

        skills_html += (
            f'<span class="skill-pill">'
            f'{skill}'
            f'</span>'
        )


    skills_html += """
</div>

</div>
"""


    render_html(
        skills_html
    )


# ============================================================
# EDUCATION & EXPERIENCE
# ============================================================

render_html(
    """
<div class="section">

<div class="section-heading">
🎓 Education & Experience
</div>

</div>
"""
)


education_col, experience_col = st.columns(2)


with education_col:

    render_html(
        """
<div class="info-panel">

<div class="info-title">
🎓 B.E. — Computer Science & Engineering
</div>

<div class="info-company">
Artificial Intelligence & Machine Learning
</div>

<div class="info-text">

<strong>CGPA:</strong> 7.9

&nbsp;&nbsp; • &nbsp;&nbsp;

<strong>Expected Graduation:</strong> 2027

</div>

</div>
"""
    )


with experience_col:

    render_html(
        """
<div class="info-panel">

<div class="info-title">
🤖 Artificial Intelligence Intern
</div>

<div class="info-company">
UNLOX
</div>

<div class="info-text">

Currently working in the AI domain and gaining
practical exposure to artificial intelligence
and related technologies.

</div>

</div>
"""
    )


# ============================================================
# CERTIFICATIONS
# ============================================================

render_html(
    """
<div class="section">

<div class="section-heading">
📜 Certifications & Activities
</div>

<div class="section-subtitle">
Learning milestones and technical activities.
</div>

</div>
"""
)


certifications = [

    "Programming in Java — NPTEL, IIT Kharagpur",

    "Social Networks — NPTEL, IIT Madras",

    "Getting Started with Artificial Intelligence — IBM SkillsBuild",

    "TECH TRIAD 2025",

    "MONAITHON 2025",

    "HackMITTEN 2.0 2025",

]


for index, certification in enumerate(
    certifications,
    start=1,
):

    render_html(
        f"""
<div class="certification">

<strong>
{index:02d}
</strong>

&nbsp;&nbsp;

🏆 {certification}

</div>
"""
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

render_html(
    """
<div class="final-card">

<div class="final-title">
🚀 Build. Learn. Improve. Repeat.
</div>

<div class="final-text">

I believe the best way to learn technology is
to build real things with it.

Every project is an opportunity to experiment,
solve problems, understand new technologies,
and become better.

My goal is to continue growing as an AI/ML
developer while building intelligent systems
that solve practical problems.

</div>

</div>
"""
)


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
<div class="footer">

🤖 AI Resume Analyzer

<br><br>

Designed & Developed by
<strong>Jagadeesh Nayak V </strong>

</div>
"""
)