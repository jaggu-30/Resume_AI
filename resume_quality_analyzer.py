"""
resume_quality_analyzer.py
==========================
Provides two independent analyses:

1. Resume Quality Review
   Detects generic phrases, repetition, buzzwords, weak descriptions,
   and missing measurable achievements.

2. AI-Writing / Originality Review
   Provides qualitative indicators of writing that may appear generic,
   formulaic, or AI-assisted.

IMPORTANT DISCLAIMER
--------------------
These analyses are OBSERVATIONAL and HEURISTIC.
• The system CANNOT determine with certainty whether content was AI-generated.
• No percentage is claimed for AI generation.
• Results are expressed as LOW / MODERATE / HIGH qualitative levels.
• The goal is to help writers make resumes more specific and authentic —
  NOT to help bypass or evade AI detection tools.
"""

import re
from collections import Counter


# ------------------------------------------------------------------
# WORDLISTS
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
    "proactive",
    "synergy",
    "leverage",
    "seek a challenging",
    "seeking a position",
    "looking for an opportunity",
    "proven track record",
    "extensive experience",
    "highly motivated",
    "exceptional leadership",
    "strategic thinker",
    "thought leader",
]

BUZZWORDS = [
    "synergy",
    "leverage",
    "paradigm",
    "disruptive",
    "innovative",
    "revolutionize",
    "cutting-edge",
    "state-of-the-art",
    "best-in-class",
    "world-class",
    "next-generation",
    "game-changing",
    "transformational",
    "holistic",
    "robust",
    "scalable",
    "end-to-end",
    "best practices",
    "agile",
    "dynamic",
    "passionate",
    "enthusiastic",
    "ecosystem",
    "bandwidth",
    "move the needle",
    "circle back",
    "deep dive",
    "low-hanging fruit",
    "take offline",
    "boil the ocean",
    "actionable insights",
    "value-add",
    "pivot",
]

AI_TRANSITION_PHRASES = [
    "moreover",
    "furthermore",
    "in conclusion",
    "in summary",
    "it is worth noting",
    "needless to say",
    "it is important to note",
    "plays a crucial role",
    "plays an important role",
    "demonstrates proficiency",
    "showcases expertise",
    "possesses strong",
    "adept at",
    "in addition to this",
    "as previously mentioned",
    "on the other hand",
    "it goes without saying",
]

ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "created",
    "managed", "led", "improved", "analyzed", "deployed",
    "optimized", "automated", "researched", "collaborated",
    "presented", "trained", "delivered", "integrated", "launched",
    "maintained", "reduced", "increased", "achieved", "contributed",
    "engineered", "architected", "coordinated", "spearheaded",
    "streamlined", "resolved", "mentored", "documented", "tested",
    "debugged", "reviewed", "migrated", "configured", "monitored",
]


# ------------------------------------------------------------------
# QUALITATIVE LEVEL HELPER
# ------------------------------------------------------------------

def _level(value, low_threshold, high_threshold):
    """
    Map a numeric value to a qualitative level string.
    Low  → value <  low_threshold
    Moderate → low_threshold <= value < high_threshold
    High → value >= high_threshold
    """
    if value < low_threshold:
        return "Low"
    elif value < high_threshold:
        return "Moderate"
    else:
        return "High"


# ------------------------------------------------------------------
# RESUME QUALITY REVIEW
# ------------------------------------------------------------------

def _count_generic_phrases(text_lower: str) -> list:
    found = []
    for phrase in GENERIC_PHRASES:
        if phrase in text_lower:
            found.append(phrase)
    return found


def _count_buzzwords(text_lower: str) -> list:
    found = []
    for word in BUZZWORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
            found.append(word)
    return found


def _count_quantified_achievements(text: str) -> int:
    """
    Count bullet/sentence patterns that contain measurable numbers
    combined with result-indicating words.
    E.g., "improved accuracy by 20%", "reduced load time by 3x",
          "managed a team of 5", "saved $10,000".
    """
    patterns = [
        r"\d+\s*%",                     # percentages: 20%, 95%
        r"\d+\s*x\b",                   # multipliers: 3x, 10x
        r"\$\s*\d+",                     # dollar amounts
        r"\b\d{4}\b",                   # years (already caught elsewhere)
        r"\bteam\s+of\s+\d+",           # team of N
        r"\b\d+\+\s*(users|clients|records|projects|students|employees)",
        r"(reduced|improved|increased|decreased|grew|saved|accelerated).*\d+",
    ]
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, text, re.IGNORECASE))
    # Subtract year matches to avoid over-counting
    year_matches = len(re.findall(r"\b\d{4}\b", text))
    count = max(0, count - year_matches)
    return count


def _count_repeated_phrases(text: str, top_n: int = 5) -> list:
    """
    Find the most-repeated 3-word phrases (trigrams) in the resume.
    Returns phrases that appear 2+ times.
    """
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    trigrams = [
        " ".join(words[i:i+3])
        for i in range(len(words) - 2)
    ]
    counter = Counter(trigrams)
    return [
        (phrase, count)
        for phrase, count in counter.most_common(top_n)
        if count >= 2
    ]


def _count_action_verbs(text: str) -> int:
    text_lower = text.lower()
    return sum(
        1 for v in ACTION_VERBS
        if re.search(r"\b" + v + r"\b", text_lower)
    )


def analyze_resume_quality(text: str) -> dict:
    """
    Perform a Resume Quality Review on the extracted resume text.

    Parameters
    ----------
    text : str
        Raw extracted resume text.

    Returns
    -------
    dict with keys:
        generic_phrases      : list of str
        generic_count        : int
        buzzwords_found      : list of str
        buzzword_count       : int
        repeated_phrases     : list of (str, int)
        quantified_count     : int
        action_verb_count    : int
        quality_levels       : dict  {metric: level-string}
        suggestions          : list of str
    """
    text_lower = text.lower()
    word_count = len(text.split())

    generic_phrases = _count_generic_phrases(text_lower)
    buzzwords_found = _count_buzzwords(text_lower)
    repeated_phrases = _count_repeated_phrases(text)
    quant_count = _count_quantified_achievements(text)
    action_count = _count_action_verbs(text)

    # Buzzword density per 100 words
    bw_density = (len(buzzwords_found) / max(word_count, 1)) * 100

    quality_levels = {
        "Generic Phrases":           _level(len(generic_phrases), 1, 3),
        "Buzzword Density":          _level(bw_density, 1, 3),
        "Repetition":                _level(len(repeated_phrases), 1, 3),
        "Quantified Achievements":   _level(quant_count, 2, 5),
        "Action-Oriented Language":  _level(action_count, 3, 7),
        "Technical Specificity":     _level(action_count + quant_count, 3, 8),
    }

    # Build suggestions
    suggestions = []
    if len(generic_phrases) >= 1:
        suggestions.append(
            f"Remove generic phrases ({len(generic_phrases)} found, "
            f"e.g. '{generic_phrases[0]}'). Replace with specific actions and results."
        )
    if bw_density >= 1:
        suggestions.append(
            "Reduce buzzword usage. Be specific about what you actually did and the tools you used."
        )
    if quant_count < 2:
        suggestions.append(
            "Add measurable achievements. Examples: 'Improved model accuracy by 12%', "
            "'Reduced API latency by 40ms', 'Automated 3 reporting workflows'."
        )
    if action_count < 3:
        suggestions.append(
            "Start bullet points with strong action verbs: "
            "Developed, Built, Designed, Optimized, Analyzed, Deployed."
        )
    if len(repeated_phrases) >= 2:
        suggestions.append(
            f"Reduce repeated wording. The phrase "
            f"'{repeated_phrases[0][0]}' appears {repeated_phrases[0][1]} times."
        )
    if not suggestions:
        suggestions.append(
            "Good writing quality detected. Keep descriptions specific and result-oriented."
        )

    return {
        "generic_phrases":    generic_phrases,
        "generic_count":      len(generic_phrases),
        "buzzwords_found":    buzzwords_found,
        "buzzword_count":     len(buzzwords_found),
        "repeated_phrases":   repeated_phrases,
        "quantified_count":   quant_count,
        "action_verb_count":  action_count,
        "quality_levels":     quality_levels,
        "suggestions":        suggestions,
    }


# ------------------------------------------------------------------
# AI-WRITING / ORIGINALITY REVIEW
# ------------------------------------------------------------------

def _detect_sentence_uniformity(text: str) -> str:
    """
    AI-generated text often has very uniform sentence lengths.
    Returns 'Low' / 'Moderate' / 'High' uniformity.
    """
    sentences = re.split(r"[.!?]+", text)
    lengths = [len(s.split()) for s in sentences if len(s.split()) >= 3]
    if len(lengths) < 3:
        return "Unknown"
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    std_dev = variance ** 0.5
    # Low std_dev relative to avg → high uniformity (AI-like)
    ratio = std_dev / avg if avg else 1
    if ratio >= 0.5:
        return "Low"   # diverse sentence lengths → good
    elif ratio >= 0.25:
        return "Moderate"
    else:
        return "High"  # very uniform → possibly AI-like


def _count_ai_transitions(text_lower: str) -> list:
    found = []
    for phrase in AI_TRANSITION_PHRASES:
        if phrase in text_lower:
            found.append(phrase)
    return found


def analyze_ai_writing(text: str) -> dict:
    """
    AI-Writing / Originality Review.

    Returns qualitative INDICATORS — not a percentage or verdict.
    This is intended to help writers identify generic patterns
    and replace them with authentic, specific content.

    Parameters
    ----------
    text : str
        Raw extracted resume text.

    Returns
    -------
    dict with keys:
        indicators       : dict  {label: level-string}
        ai_transitions   : list of str
        suggestions      : list of str
        disclaimer       : str
    """
    text_lower = text.lower()
    word_count = len(text.split())

    generic_phrases = _count_generic_phrases(text_lower)
    buzzwords_found = _count_buzzwords(text_lower)
    ai_transitions  = _count_ai_transitions(text_lower)
    quant_count     = _count_quantified_achievements(text)
    action_count    = _count_action_verbs(text)
    sentence_unif   = _detect_sentence_uniformity(text)

    # Generic wording level
    generic_level = _level(len(generic_phrases) + len(buzzwords_found), 2, 5)

    # Transition phrase density per 100 words
    trans_density = (len(ai_transitions) / max(word_count, 1)) * 100
    transition_level = _level(trans_density, 0.5, 1.5)

    # Quantification → inverse: more = better (lower AI-generic risk)
    quant_level = _level(quant_count, 2, 5)   # Low/Moderate/High quant
    # For display we invert: "High" quantification is GOOD
    specificity_level = _level(action_count + quant_count, 3, 8)

    indicators = {
        "Generic Wording":         generic_level,
        "Repetition":              _level(
                                       len(_count_repeated_phrases(text)), 1, 3
                                   ),
        "AI Transition Phrases":   transition_level,
        "Sentence Variety":        sentence_unif,
        "Quantified Achievements": quant_level,   # Low = needs improvement
        "Specificity":             specificity_level,
        "Action-Oriented Language":_level(action_count, 3, 7),
    }

    suggestions = [
        "Replace generic statements with specific actions, tools, and measurable outcomes.",
        "Mention the actual tools, frameworks, and datasets you used.",
        "Add real numbers and metrics: accuracy %, time saved, users served, records processed.",
        "Describe your personal contribution — what *you* specifically built or decided.",
        "Vary sentence length and structure to reflect authentic writing.",
        "Avoid AI-style transitions ('Moreover', 'Furthermore', 'It is worth noting').",
    ]

    # Only keep relevant suggestions
    filtered = []
    if generic_level in ("Moderate", "High"):
        filtered.append(suggestions[0])
        filtered.append(suggestions[1])
    if quant_level == "Low":
        filtered.append(suggestions[2])
    filtered.append(suggestions[3])
    if sentence_unif == "High":
        filtered.append(suggestions[4])
    if transition_level in ("Moderate", "High"):
        filtered.append(suggestions[5])
    if not filtered:
        filtered = [
            "Writing appears specific and authentic. "
            "Continue describing real tools, actions, and results."
        ]

    disclaimer = (
        "This review identifies common patterns that may reduce resume authenticity. "
        "It does NOT determine whether content was AI-generated, "
        "and does NOT produce an AI-generation percentage. "
        "Results are observational only."
    )

    return {
        "indicators":    indicators,
        "ai_transitions": ai_transitions,
        "suggestions":   filtered,
        "disclaimer":    disclaimer,
    }
