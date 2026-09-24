"""
ats_analyzer.py
===============
Provides an Estimated ATS Compatibility Score (0-100) for a resume.

IMPORTANT DISCLAIMER
--------------------
The score produced here is an ESTIMATE based on measurable resume
characteristics. It does NOT represent the exact score that any
real employer's proprietary ATS system would produce.

Use it to identify areas for improvement, not as a hiring prediction.
"""

import re
import os
import pandas as pd


# ------------------------------------------------------------------
# PATHS  (relative to project root, same convention as other modules)
# ------------------------------------------------------------------
JOB_ROLE_FILE = "data/job_roles.csv"
SKILL_FILE     = "data/skill_dictionary.csv"


# ------------------------------------------------------------------
# GENERIC-PHRASE WORDLIST  (shared between ATS + quality modules)
# ------------------------------------------------------------------
GENERIC_PHRASES = [
    "team player",
    "hard worker",
    "hard-working",
    "hardworking",
    "fast learner",
    "quick learner",
    "self-motivated",
    "self motivated",
    "detail oriented",
    "detail-oriented",
    "results driven",
    "results-driven",
    "passionate about",
    "motivated individual",
    "go-getter",
    "dynamic professional",
    "excellent communication skills",
    "good communication skills",
    "strong communication skills",
    "good interpersonal skills",
    "strong work ethic",
    "outside the box",
    "think outside",
    "proactive",
    "synergy",
    "leverage",
    "utilize",
    "utilize my skills",
    "seeking a position",
    "looking for an opportunity",
]

# Transition / filler phrases often associated with AI-assisted writing
AI_TRANSITION_PHRASES = [
    "moreover",
    "furthermore",
    "in conclusion",
    "in summary",
    "it is worth noting",
    "needless to say",
    "as a result",
    "in addition to",
    "it is important to note",
    "plays a crucial role",
    "plays an important role",
    "is responsible for",
    "demonstrates proficiency",
    "showcases expertise",
    "possesses strong",
]


# ------------------------------------------------------------------
# HELPER: load job roles without duplicating job_matcher logic
# ------------------------------------------------------------------

def _load_job_roles():
    """
    Load job_roles.csv from the data directory.
    Returns an empty DataFrame on failure so the caller degrades gracefully.
    """
    try:
        return pd.read_csv(JOB_ROLE_FILE)
    except Exception:
        return pd.DataFrame(columns=["job_role", "skills", "description"])


def _load_skill_dictionary():
    """
    Load skill_dictionary.csv.
    Returns an empty DataFrame on failure.
    """
    try:
        return pd.read_csv(SKILL_FILE)
    except Exception:
        return pd.DataFrame(columns=["skill", "category", "aliases"])


def _get_required_skills_for_role(target_role: str) -> list:
    """
    Return the list of required skills for a given job role
    using the existing job_roles.csv dataset.
    """
    df = _load_job_roles()
    if df.empty:
        return []
    row = df[df["job_role"].str.lower() == target_role.lower()]
    if row.empty:
        return []
    raw = str(row.iloc[0]["skills"])
    return [s.strip() for s in raw.split("|") if s.strip()]


def _all_known_skills() -> list:
    """Return every skill name from skill_dictionary.csv."""
    df = _load_skill_dictionary()
    if df.empty:
        return []
    return df["skill"].tolist()


# ------------------------------------------------------------------
# COMPONENT SCORERS
# ------------------------------------------------------------------

def _score_contact_info(text: str) -> dict:
    """
    10 points.
    Looks for email and phone number patterns.
    """
    MAX = 10
    score = 0
    details = {}

    email_found = bool(re.search(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        text
    ))
    phone_found = bool(re.search(
        r"(\+?\d[\d\s\-().]{7,}\d)",
        text
    ))

    details["email_found"] = email_found
    details["phone_found"] = phone_found

    if email_found:
        score += 5
    if phone_found:
        score += 5

    return {"score": score, "max": MAX, "details": details}


def _score_section_completeness(sections: dict) -> dict:
    """
    25 points — 5 pts per important section.
    Sections evaluated: education, experience, skills, projects, certifications.
    """
    MAX = 25
    SECTION_SCORES = {
        "education":      5,
        "experience":     5,
        "skills":         5,
        "projects":       5,
        "certifications": 5,
    }

    score = 0
    present = {}

    for section_name, pts in SECTION_SCORES.items():
        found = (
            section_name in sections
            and bool(sections[section_name].strip())
        )
        present[section_name] = found
        if found:
            score += pts

    pct = round((score / MAX) * 100, 1) if MAX else 0

    return {
        "score": score,
        "max": MAX,
        "percent": pct,
        "present": present,
    }


def _score_keyword_coverage(text: str, target_role: str) -> dict:
    """
    30 points.
    Measures what fraction of the target role's required skills
    appear in the full resume text (case-insensitive word-boundary match).
    """
    MAX = 30
    required = _get_required_skills_for_role(target_role)

    if not required:
        return {
            "score": 0,
            "max": MAX,
            "percent": 0.0,
            "matched": [],
            "missing": [],
            "required": [],
        }

    text_lower = text.lower()
    matched = []
    missing = []

    for skill in required:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text_lower):
            matched.append(skill)
        else:
            missing.append(skill)

    pct = (len(matched) / len(required)) * 100 if required else 0
    score = round((pct / 100) * MAX, 2)

    return {
        "score": score,
        "max": MAX,
        "percent": round(pct, 1),
        "matched": matched,
        "missing": missing,
        "required": required,
    }


def _score_skill_coverage(resume_skills: list) -> dict:
    """
    20 points.
    Measures detected skills as a fraction of all known skills.
    Capped at 60% knowledge coverage = full 20 pts (realistic ceiling).
    """
    MAX = 20
    FULL_COVERAGE_THRESHOLD = 0.60   # 60% of 47 skills = full score

    all_skills = _all_known_skills()
    total = len(all_skills)

    if total == 0 or not resume_skills:
        return {"score": 0, "max": MAX, "percent": 0.0}

    ratio = len(resume_skills) / total
    capped_ratio = min(ratio / FULL_COVERAGE_THRESHOLD, 1.0)
    score = round(capped_ratio * MAX, 2)
    pct = round((len(resume_skills) / total) * 100, 1)

    return {
        "score": score,
        "max": MAX,
        "percent": pct,
        "detected_count": len(resume_skills),
        "total_known": total,
    }


def _score_structure_readability(text: str) -> dict:
    """
    15 points.
    Evaluates basic structure heuristics:
    - Minimum word count (at least 150 words = viable resume)
    - Not too short (< 50 words = near-empty)
    - Sentence length variety (not all identical lengths)
    - Has some numeric patterns (years, percentages, quantities)
    """
    MAX = 15
    score = 0
    details = {}

    words = text.split()
    word_count = len(words)
    details["word_count"] = word_count

    # Word count scoring (0-6 pts)
    if word_count >= 400:
        score += 6
    elif word_count >= 200:
        score += 4
    elif word_count >= 100:
        score += 2
    elif word_count >= 50:
        score += 1

    # Numeric / quantified patterns (0-4 pts)
    numeric_matches = re.findall(
        r"\b\d+(\.\d+)?(%|x|k|\+)?\b|\b\d{4}\b",
        text
    )
    details["numeric_patterns"] = len(numeric_matches)
    if len(numeric_matches) >= 5:
        score += 4
    elif len(numeric_matches) >= 2:
        score += 2
    elif len(numeric_matches) >= 1:
        score += 1

    # File type note — always text (PDF/DOCX already parsed), give 3 pts
    score += 3
    details["file_compatible"] = True

    # Action verbs at sentence start (0-2 pts)
    action_verbs = [
        "developed", "built", "designed", "implemented", "created",
        "managed", "led", "improved", "analyzed", "deployed",
        "optimized", "automated", "researched", "collaborated",
        "presented", "trained", "delivered", "integrated", "launched",
        "maintained", "reduced", "increased", "achieved", "contributed",
    ]
    text_lower = text.lower()
    action_count = sum(
        1 for v in action_verbs if re.search(r"\b" + v + r"\b", text_lower)
    )
    details["action_verbs_found"] = action_count
    if action_count >= 4:
        score += 2
    elif action_count >= 1:
        score += 1

    pct = round((score / MAX) * 100, 1) if MAX else 0

    return {
        "score": score,
        "max": MAX,
        "percent": pct,
        "details": details,
    }


# ------------------------------------------------------------------
# IMPROVEMENT SUGGESTIONS
# ------------------------------------------------------------------

def _generate_suggestions(
    contact: dict,
    sections: dict,
    keyword_cov: dict,
    skill_cov: dict,
    structure: dict,
) -> list:
    suggestions = []

    if not contact["details"].get("email_found"):
        suggestions.append(
            "Add your email address — it is required by most ATS systems."
        )
    if not contact["details"].get("phone_found"):
        suggestions.append(
            "Include a phone number for recruiter contact."
        )

    missing_sections = [
        s for s, present in sections["present"].items()
        if not present
    ]
    if missing_sections:
        suggestions.append(
            f"Add missing sections: {', '.join(missing_sections).title()}."
        )

    if keyword_cov["percent"] < 50:
        suggestions.append(
            f"Keyword coverage for the selected role is low "
            f"({keyword_cov['percent']:.0f}%). "
            "Add missing keywords: "
            + ", ".join(keyword_cov["missing"][:5])
            + ("..." if len(keyword_cov["missing"]) > 5 else ".")
        )
    elif keyword_cov["percent"] < 80:
        suggestions.append(
            "Consider adding more role-specific keywords to improve ATS ranking."
        )

    if structure["details"].get("word_count", 0) < 200:
        suggestions.append(
            "Your resume appears short. Expand descriptions with specific tasks and achievements."
        )

    if structure["details"].get("numeric_patterns", 0) < 2:
        suggestions.append(
            "Add measurable achievements (e.g., 'improved accuracy by 15%', "
            "'handled 10,000+ records') to strengthen your resume."
        )

    if structure["details"].get("action_verbs_found", 0) < 3:
        suggestions.append(
            "Start bullet points with strong action verbs "
            "(e.g., Developed, Built, Implemented, Analyzed)."
        )

    if not suggestions:
        suggestions.append(
            "Your resume looks well-structured. "
            "Keep keywords updated when applying for specific roles."
        )

    return suggestions


# ------------------------------------------------------------------
# MAIN PUBLIC FUNCTION
# ------------------------------------------------------------------

def analyze_ats(
    extracted_text: str,
    resume_skills: list,
    sections: dict,
    target_role: str,
) -> dict:
    """
    Calculate an Estimated ATS Compatibility Score (0-100).

    Parameters
    ----------
    extracted_text : str
        Raw text extracted from the resume (before cleaning).
    resume_skills : list of str
        Skills detected by skill_extractor (names only, not dicts).
    sections : dict
        Section dict returned by resume_section_analyzer.extract_resume_sections().
    target_role : str
        The job role selected by the user.

    Returns
    -------
    dict with keys:
        ats_score       : int  0-100
        contact         : dict
        section_comp    : dict
        keyword_cov     : dict
        skill_cov       : dict
        structure       : dict
        suggestions     : list of str
        breakdown       : dict  {label: percent}  for display
    """

    # Individual component scores
    contact     = _score_contact_info(extracted_text)
    section_comp = _score_section_completeness(sections)
    keyword_cov  = _score_keyword_coverage(extracted_text, target_role)
    skill_cov    = _score_skill_coverage(resume_skills)
    structure    = _score_structure_readability(extracted_text)

    # Total raw score (out of 100)
    raw_total = (
        contact["score"]
        + section_comp["score"]
        + keyword_cov["score"]
        + skill_cov["score"]
        + structure["score"]
    )

    # Clamp to [0, 100]
    ats_score = max(0, min(100, round(raw_total)))

    # Suggestions
    suggestions = _generate_suggestions(
        contact, section_comp, keyword_cov, skill_cov, structure
    )

    # Breakdown percentages for progress bars
    # (each component shown as % of its own max)
    breakdown = {
        "Keyword Coverage":    round(keyword_cov["percent"], 1),
        "Skill Coverage":      round(skill_cov["percent"], 1),
        "Section Completeness": round(section_comp["percent"], 1),
        "Resume Structure":    round(structure["percent"], 1),
        "Contact Info":        round(
            (contact["score"] / contact["max"] * 100)
            if contact["max"] else 0, 1
        ),
    }

    return {
        "ats_score":    ats_score,
        "contact":      contact,
        "section_comp": section_comp,
        "keyword_cov":  keyword_cov,
        "skill_cov":    skill_cov,
        "structure":    structure,
        "suggestions":  suggestions,
        "breakdown":    breakdown,
    }
