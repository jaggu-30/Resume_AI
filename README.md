# 🤖 AI Resume Analyzer and Job Recommendation System

An NLP-based Streamlit application that analyzes resumes, extracts technical skills, compares them with job-role requirements, recommends suitable roles, identifies skill gaps, and generates a personalized learning roadmap.

## 📌 Project Overview

Students often find it difficult to understand whether their resumes contain the skills required for their desired job roles.

This project provides an educational resume analysis system that:

- Extracts text from PDF and DOCX resumes
- Cleans and normalizes resume text
- Detects technical and job-related skills
- Categorizes detected skills
- Compares resume skills with multiple job roles
- Calculates role match scores
- Recommends the top three suitable roles
- Identifies matched and missing skills
- Generates a learning roadmap
- Provides learning resources
- Generates a downloadable PDF analysis report

> **Important:** Match scores are estimates for learning and self-improvement. They are not hiring or rejection decisions.

---

## 🎯 Objectives

The main objectives of the project are:

1. Extract information from PDF and DOCX resumes.
2. Clean and normalize unstructured resume text.
3. Identify technical skills using controlled keyword matching.
4. Compare resumes with predefined job-role requirements.
5. Calculate resume-to-role match scores.
6. Recommend suitable job roles.
7. Identify skill gaps for a selected target role.
8. Generate a simple learning roadmap.
9. Provide an interactive Streamlit dashboard.

---

## ✨ Features

### 📄 Resume Upload

- Supports PDF resumes
- Supports DOCX resumes
- Validates file type
- Validates file size
- Displays uploaded filename
- Processes resumes temporarily without permanent storage

### 📝 Resume Text Extraction

PDF files are processed using `pypdf`.

DOCX files are processed using `python-docx`.

### 🧹 Text Cleaning

The cleaning pipeline:

- Converts text to lowercase
- Removes unnecessary symbols
- Removes repeated whitespace
- Normalizes technical terms
- Preserves important terms such as C++, C#, and .NET

### 🧠 Skill Extraction

The system uses a controlled skill dictionary containing 47 job-related technical skills.

Skills are grouped into categories such as:

- Programming
- Database
- Data
- Machine Learning
- Artificial Intelligence
- Backend
- Cloud
- Tools

### 💼 Job Role Dataset

The application currently evaluates nine predefined job roles:

1. Data Analyst
2. Machine Learning Engineer
3. AI Engineer
4. NLP Engineer
5. Computer Vision Engineer
6. Python Developer
7. Data Scientist
8. Backend Developer
9. AI/ML Intern

Each role contains required skills and a role description.

### 📊 Hybrid Resume Matching

The matching engine combines two signals:

**1. Skill Overlap**

Measures how many required role skills are already present in the resume.

**2. TF-IDF + Cosine Similarity**

Converts resume skills and job-role requirements into numerical vectors and measures their similarity.

The final score combines both signals:

```text
Final Score =
    70% Skill Overlap
    +
    30% TF-IDF Similarity