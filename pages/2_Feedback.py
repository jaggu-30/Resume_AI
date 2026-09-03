import streamlit as st
from navigation import top_navigation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Feedback | AI Resume Analyzer",
    page_icon="💬",
    layout="wide",
)


# ============================================================
# TOP NAVIGATION
# ============================================================

top_navigation("feedback")


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page width */
    .block-container {
        max-width: 1100px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }


    /* Feedback hero */
    .feedback-hero {
        text-align: center;
        padding: 45px 20px 35px 20px;
    }

    .feedback-icon {
        font-size: 3.5rem;
        margin-bottom: 5px;
    }

    .feedback-title {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(
            90deg,
            #4facfe,
            #8f7cff,
            #00f2fe
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .feedback-subtitle {
        max-width: 650px;
        margin: 15px auto 0 auto;
        color: #a7afbd;
        font-size: 1.05rem;
        line-height: 1.7;
    }


    /* Cards */
    .feedback-card {
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 20px;
        padding: 25px;
        background: rgba(255, 255, 255, 0.025);
        min-height: 150px;
    }

    .feedback-card h3 {
        margin-top: 0;
        font-size: 1.25rem;
    }

    .feedback-card p {
        color: #a7afbd;
        line-height: 1.6;
    }


    /* Rating */
    .rating-box {
        text-align: center;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        background: rgba(255, 255, 255, 0.025);
        margin-top: 15px;
    }

    .rating-number {
        font-size: 2.5rem;
        font-weight: 900;
    }


    /* Footer */
    .feedback-footer {
        text-align: center;
        color: #6f7785;
        padding-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="feedback-hero">',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="feedback-icon">💬</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="feedback-title">Share Your Feedback</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="feedback-subtitle">
        Your feedback helps improve the AI Resume Analyzer.
        Tell us what you liked, what can be improved,
        or what features you would like to see next.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# EXPERIENCE + CATEGORY
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        <div class="feedback-card">
            <h3>⭐ Rate Your Experience</h3>
            <p>
                How would you rate your overall experience
                with the AI Resume Analyzer?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rating = st.slider(
        "Rating",
        min_value=1,
        max_value=5,
        value=5,
        step=1,
    )

    st.markdown(
        f"""
        <div class="rating-box">
            <div class="rating-number">
                {"⭐" * rating}
            </div>
            <div>
                {rating} / 5
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="feedback-card">
            <h3>🎯 Feedback Category</h3>
            <p>
                Select the area your feedback is related to.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feedback_type = st.selectbox(
        "Category",
        [
            "General Feedback",
            "UI / Design",
            "Resume Analysis",
            "Job Recommendations",
            "Skill Gap Analysis",
            "Learning Resources",
            "Bug Report",
            "Feature Request",
        ],
    )


st.write("")


# ============================================================
# FEEDBACK FORM
# ============================================================

st.subheader("📝 Tell Us More")

feedback = st.text_area(
    "Your Feedback",
    placeholder=(
        "Example: The resume analysis was useful, "
        "but I would like more learning resources..."
    ),
    height=180,
)


name = st.text_input(
    "Your Name (Optional)",
    placeholder="Enter your name",
)


email = st.text_input(
    "Email (Optional)",
    placeholder="Enter your email",
)


# ============================================================
# SUBMIT
# ============================================================

st.write("")


if st.button(
    "🚀 Submit Feedback",
    type="primary",
    use_container_width=True,
):

    if not feedback.strip():

        st.warning(
            "Please enter your feedback before submitting."
        )

    else:

        st.success(
            "🎉 Thank you for your feedback!"
        )

        st.balloons()

        st.markdown(
            f"""
            ### ✅ Feedback Submitted

            **Rating:** {"⭐" * rating}

            **Category:** {feedback_type}

            **Message:** {feedback}
            """
        )

        if name.strip():

            st.write(
                f"**Name:** {name}"
            )

        if email.strip():

            st.write(
                f"**Email:** {email}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="feedback-footer">
        🤖 AI Resume Analyzer
        <br>
        Built to help students understand their skills,
        career matches, and learning opportunities.
    </div>
    """,
    unsafe_allow_html=True,
)