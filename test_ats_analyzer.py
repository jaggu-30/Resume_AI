"""
test_ats_analyzer.py
====================
Tests for ats_analyzer.py and resume_quality_analyzer.py.

Run with:
    python -m pytest test_ats_analyzer.py -v

These tests do NOT require Streamlit or any running server.
"""

import pytest
import sys
import os

# Ensure imports resolve from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ats_analyzer import analyze_ats
from resume_quality_analyzer import analyze_resume_quality, analyze_ai_writing


# ------------------------------------------------------------------
# FIXTURES
# ------------------------------------------------------------------

FULL_SECTIONS = {
    "education":      "B.Tech Computer Science, XYZ University, 2022",
    "experience":     "Software Engineer Intern at ABC Corp, June 2022 - Aug 2022",
    "skills":         "Python, Machine Learning, SQL, Pandas, NumPy",
    "projects":       "Built a sentiment analysis model using BERT. Deployed with FastAPI.",
    "certifications": "AWS Certified Cloud Practitioner",
}

MINIMAL_SECTIONS = {
    "skills": "Python",
}

EMPTY_SECTIONS = {}

RICH_RESUME_TEXT = """
John Doe
john.doe@email.com
+91 9876543210

Education
B.Tech Computer Science, XYZ University, 2022

Skills
Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL, Docker

Experience
Machine Learning Intern at ABC Corp (June 2022 – Aug 2022)
- Developed a sentiment analysis pipeline using Python and Scikit-learn.
- Improved model accuracy by 18% through hyperparameter tuning.
- Reduced data preprocessing time by 40% using Pandas vectorization.
- Automated weekly reporting for a team of 5 data scientists.

Projects
Resume Classifier – Built a resume classification model using TF-IDF and Logistic Regression.
Deployed on FastAPI with Docker. Achieved 92% accuracy on test data.

Certifications
AWS Certified Cloud Practitioner
""".strip()

MINIMAL_RESUME_TEXT = "Python developer. Good communication skills."

EMPTY_RESUME_TEXT = ""

GENERIC_HEAVY_TEXT = """
I am a hardworking, self-motivated team player with a proven track record.
I am passionate about technology. I am a fast learner with excellent communication skills.
Moreover, I possess strong interpersonal skills. Furthermore, I am results-driven and detail-oriented.
In conclusion, I am a dynamic professional with a holistic approach.
"""

TARGET_ROLE_FULL_MATCH    = "Machine Learning Engineer"  # needs Python, ML, Sklearn, Pandas, Numpy, FastAPI, Docker
TARGET_ROLE_NO_MATCH      = "Computer Vision Engineer"   # needs OpenCV, CNN, YOLO, PyTorch, Deep Learning


# ------------------------------------------------------------------
# TEST 1: Empty resume
# ------------------------------------------------------------------
def test_empty_resume_does_not_crash():
    """ATS analysis on an empty resume must not raise an exception."""
    result = analyze_ats(
        extracted_text=EMPTY_RESUME_TEXT,
        resume_skills=[],
        sections=EMPTY_SECTIONS,
        target_role="Data Analyst",
    )
    assert isinstance(result, dict), "Result should be a dict"
    assert "ats_score" in result


# ------------------------------------------------------------------
# TEST 2: ATS score is always between 0 and 100
# ------------------------------------------------------------------
@pytest.mark.parametrize("text,skills,sections,role", [
    (EMPTY_RESUME_TEXT,   [],              EMPTY_SECTIONS,   "Data Analyst"),
    (MINIMAL_RESUME_TEXT, ["Python"],      MINIMAL_SECTIONS, "Data Analyst"),
    (RICH_RESUME_TEXT,    ["Python", "Machine Learning", "Pandas", "NumPy",
                           "Scikit-learn", "Docker", "FastAPI"],
                          FULL_SECTIONS,   "Machine Learning Engineer"),
    (GENERIC_HEAVY_TEXT,  [],              EMPTY_SECTIONS,   "NLP Engineer"),
])
def test_ats_score_bounds(text, skills, sections, role):
    """ATS score must always be in [0, 100]."""
    result = analyze_ats(text, skills, sections, role)
    score = result["ats_score"]
    assert 0 <= score <= 100, f"Score {score} is out of [0,100] range"


# ------------------------------------------------------------------
# TEST 3: Resume with complete sections scores higher on section completeness
# ------------------------------------------------------------------
def test_complete_sections_score_higher():
    result_full = analyze_ats(RICH_RESUME_TEXT, ["Python"], FULL_SECTIONS, "Data Analyst")
    result_empty = analyze_ats(MINIMAL_RESUME_TEXT, ["Python"], EMPTY_SECTIONS, "Data Analyst")
    assert (
        result_full["section_comp"]["score"]
        > result_empty["section_comp"]["score"]
    ), "Full sections should score higher than empty sections"


# ------------------------------------------------------------------
# TEST 4: Resume with missing sections
# ------------------------------------------------------------------
def test_missing_sections_detected():
    result = analyze_ats(MINIMAL_RESUME_TEXT, ["Python"], MINIMAL_SECTIONS, "Data Analyst")
    present = result["section_comp"]["present"]
    # Only 'skills' is present; others should be False
    assert present.get("skills") is True
    assert present.get("education") is False
    assert present.get("experience") is False
    assert present.get("projects") is False
    assert present.get("certifications") is False


# ------------------------------------------------------------------
# TEST 5: Many matching skills → high keyword coverage
# ------------------------------------------------------------------
def test_many_matching_skills_high_coverage():
    # ML Engineer requires: Python, ML, Sklearn, Pandas, Numpy, FastAPI, Docker
    result = analyze_ats(
        RICH_RESUME_TEXT,
        ["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn", "FastAPI", "Docker"],
        FULL_SECTIONS,
        TARGET_ROLE_FULL_MATCH,
    )
    # Keyword coverage percent should be above 50%
    assert result["keyword_cov"]["percent"] >= 50, (
        f"Expected keyword coverage >= 50% for a well-matched resume, "
        f"got {result['keyword_cov']['percent']}%"
    )


# ------------------------------------------------------------------
# TEST 6: Few matching skills → lower keyword coverage
# ------------------------------------------------------------------
def test_few_matching_skills_lower_coverage():
    result_full  = analyze_ats(RICH_RESUME_TEXT, ["Python", "Machine Learning", "Pandas", "NumPy",
                                                   "Scikit-learn", "FastAPI", "Docker"],
                                FULL_SECTIONS, TARGET_ROLE_FULL_MATCH)
    result_few   = analyze_ats(MINIMAL_RESUME_TEXT, ["Python"], MINIMAL_SECTIONS, TARGET_ROLE_FULL_MATCH)
    assert (
        result_full["keyword_cov"]["percent"]
        >= result_few["keyword_cov"]["percent"]
    ), "Resume with more matching skills should have higher keyword coverage"


# ------------------------------------------------------------------
# TEST 7: No matching skills → keyword coverage is 0% or very low
# ------------------------------------------------------------------
def test_no_matching_skills():
    # Computer Vision Engineer requires: OpenCV, CNN, YOLO, PyTorch, Deep Learning, Python, Computer Vision
    result = analyze_ats(
        "I know SQL and Excel.",
        ["SQL", "Excel"],
        {"skills": "SQL, Excel"},
        TARGET_ROLE_NO_MATCH,
    )
    # SQL and Excel are not in Computer Vision Engineer's required skills
    assert result["keyword_cov"]["percent"] == 0.0, (
        f"Expected 0% keyword coverage, got {result['keyword_cov']['percent']}%"
    )


# ------------------------------------------------------------------
# TEST 8: Job-specific keyword matching — matched + missing are correct
# ------------------------------------------------------------------
def test_keyword_matching_correctness():
    # ML Engineer requires: Python, Machine Learning, Scikit-learn, Pandas, NumPy, FastAPI, Docker
    result = analyze_ats(
        "Python Machine Learning Pandas NumPy",
        ["Python", "Machine Learning", "Pandas", "NumPy"],
        MINIMAL_SECTIONS,
        TARGET_ROLE_FULL_MATCH,
    )
    matched = [s.lower() for s in result["keyword_cov"]["matched"]]
    missing = [s.lower() for s in result["keyword_cov"]["missing"]]

    assert "python" in matched
    assert "pandas" in matched
    # FastAPI and Docker should be in missing (not in the text above)
    assert "fastapi" in missing or "docker" in missing, (
        "FastAPI/Docker should appear as missing keywords"
    )


# ------------------------------------------------------------------
# TEST 9: Missing keywords are correctly identified
# ------------------------------------------------------------------
def test_missing_keywords_identified():
    result = analyze_ats(
        "I know Python.",
        ["Python"],
        MINIMAL_SECTIONS,
        "Data Scientist",   # requires: Python, SQL, Pandas, NumPy, ML, Sklearn, Statistics, Matplotlib
    )
    missing = [s.lower() for s in result["keyword_cov"]["missing"]]
    assert len(missing) > 0, "Should identify missing keywords for Data Scientist"
    # SQL is not in "I know Python." so it should be missing
    assert "sql" in missing


# ------------------------------------------------------------------
# TEST 10: Resume quality analysis runs without crashing
# ------------------------------------------------------------------
@pytest.mark.parametrize("text", [
    EMPTY_RESUME_TEXT,
    MINIMAL_RESUME_TEXT,
    RICH_RESUME_TEXT,
    GENERIC_HEAVY_TEXT,
])
def test_quality_analysis_no_crash(text):
    """analyze_resume_quality must not raise for any input."""
    result = analyze_resume_quality(text)
    assert isinstance(result, dict)
    assert "generic_count" in result
    assert "suggestions" in result
    assert isinstance(result["suggestions"], list)


# ------------------------------------------------------------------
# TEST 11: AI-writing review does not claim a percentage
# ------------------------------------------------------------------
def test_ai_writing_no_percentage_claim():
    """The AI-writing review must NOT return any field named like 'ai_percent'."""
    result = analyze_ai_writing(GENERIC_HEAVY_TEXT)
    assert "ai_percent" not in result
    assert "ai_generated_percent" not in result
    assert "percent" not in result
    assert isinstance(result["indicators"], dict)


# ------------------------------------------------------------------
# TEST 12: Generic-heavy resume is flagged
# ------------------------------------------------------------------
def test_generic_resume_flagged():
    result = analyze_resume_quality(GENERIC_HEAVY_TEXT)
    # Should detect at least 3 generic phrases
    assert result["generic_count"] >= 3, (
        f"Expected >= 3 generic phrases, got {result['generic_count']}"
    )


# ------------------------------------------------------------------
# TEST 13: Rich resume has fewer generic phrases than generic-heavy resume
# ------------------------------------------------------------------
def test_rich_resume_fewer_generic_phrases():
    rich = analyze_resume_quality(RICH_RESUME_TEXT)
    generic = analyze_resume_quality(GENERIC_HEAVY_TEXT)
    assert rich["generic_count"] <= generic["generic_count"], (
        "Rich resume should have fewer or equal generic phrases than generic-heavy text"
    )


# ------------------------------------------------------------------
# TEST 14: Suggestions list is never empty
# ------------------------------------------------------------------
@pytest.mark.parametrize("text", [
    EMPTY_RESUME_TEXT,
    RICH_RESUME_TEXT,
    GENERIC_HEAVY_TEXT,
])
def test_suggestions_never_empty(text):
    result_ats = analyze_ats(text, [], {}, "Data Analyst")
    result_quality = analyze_resume_quality(text)
    result_ai = analyze_ai_writing(text)

    assert len(result_ats["suggestions"]) >= 1
    assert len(result_quality["suggestions"]) >= 1
    assert len(result_ai["suggestions"]) >= 1
