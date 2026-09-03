import re


SECTION_ALIASES = {
    "education": [
        "education",
        "academic profile",
        "academic qualification",
        "academic qualifications",
        "educational qualification",
        "educational qualifications",
    ],

    "projects": [
        "projects",
        "project",
        "project undertaken",
        "project undertook",
        "projects undertaken",
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internships",
        "internship",
        "internships/trainings",
        "internships / trainings",
        "training",
        "trainings",
    ],

    "certifications": [
        "certifications",
        "certification",
        "additional certifications",
        "courses",
        "courses and certifications",
    ],

    "skills": [
        "skills",
        "technical skills",
        "computer literacy",
        "technical knowledge",
        "programming skills",
    ],
}


STOP_HEADINGS = [
    "achievements",
    "personal strengths",
    "regional languages known",
    "reginal languages known",
    "languages known",
    "hobbies",
    "personal profile",
]


def normalize_text(text):
    text = text.lower().strip()

    text = text.replace(":", "")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_exact_section(line):
    """
    Detect a section only when the complete line
    represents a known section heading.
    """

    normalized_line = normalize_text(line)

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            if normalized_line == normalize_text(alias):
                return section

    return None


def get_colon_section(line):
    """
    Detect headings such as:

        Internships/Trainings:
        Academic Profile:
        Additional Certifications:
        Computer Literacy:

    Only accept the heading when the colon is
    immediately after the known heading.
    """

    original_line = line.strip()

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"^\s*"
                + re.escape(alias)
                + r"\s*:"
            )

            if re.match(
                pattern,
                original_line,
                flags=re.IGNORECASE
            ):

                return section

    return None


def get_stop_heading(line):
    """
    Detect headings that mark the end of useful
    resume information.
    """

    normalized_line = normalize_text(line)

    for heading in STOP_HEADINGS:

        if normalized_line.startswith(
            normalize_text(heading)
        ):

            return True

    return False


def clean_content_lines(content):
    """
    Convert bullet points into separate,
    readable lines.
    """

    content = re.sub(
        r"[•●▪◦]",
        "\n",
        content
    )

    lines = []

    for line in content.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return lines


def extract_resume_sections(text):

    sections = {}

    current_section = None

    lines = text.splitlines()

    for line in lines:

        cleaned_line = line.strip()

        if not cleaned_line:
            continue


        # --------------------------------------------------
        # STOP HEADINGS
        # --------------------------------------------------

        if get_stop_heading(cleaned_line):

            current_section = None
            continue


        # --------------------------------------------------
        # EXACT SECTION HEADING
        # --------------------------------------------------

        section = get_exact_section(
            cleaned_line
        )

        if section:

            current_section = section

            if section not in sections:
                sections[section] = []

            continue


        # --------------------------------------------------
        # COLON SECTION HEADING
        # --------------------------------------------------

        section = get_colon_section(
            cleaned_line
        )

        if section:

            current_section = section

            if section not in sections:
                sections[section] = []

            # If there is content after the colon,
            # keep it as section content.

            aliases = SECTION_ALIASES[section]

            for alias in aliases:

                pattern = (
                    r"^\s*"
                    + re.escape(alias)
                    + r"\s*:\s*"
                )

                match = re.match(
                    pattern,
                    cleaned_line,
                    flags=re.IGNORECASE
                )

                if match:

                    remaining = cleaned_line[
                        match.end():
                    ].strip()

                    if remaining:

                        sections[section].append(
                            remaining
                        )

                    break

            continue


        # --------------------------------------------------
        # NORMAL CONTENT
        # --------------------------------------------------

        if current_section:

            sections[current_section].append(
                cleaned_line
            )


    # --------------------------------------------------
    # CLEAN FINAL CONTENT
    # --------------------------------------------------

    for section in sections:

        content = "\n".join(
            sections[section]
        )

        sections[section] = "\n".join(
            clean_content_lines(content)
        ).strip()


    return sections