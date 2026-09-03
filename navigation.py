import streamlit as st


def top_navigation(active_page):

    # Hide Streamlit's default sidebar
    st.markdown(
        """
        <style>

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        .top-nav {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            padding: 8px 0 24px 0;
            margin-bottom: 10px;
        }

        .nav-title {
            text-align: center;
            font-size: 1.05rem;
            font-weight: 800;
            margin-bottom: 8px;
            opacity: 0.9;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="nav-title">
            🤖 AI Resume Analyzer
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(
        [1, 1, 1],
        gap="small",
    )

    with col1:

        if st.button(
            "📄  AI Resume",
            use_container_width=True,
            type="primary" if active_page == "resume" else "secondary",
        ):

            if active_page != "resume":
                st.switch_page("app.py")


    with col2:

        if st.button(
            "👤  About",
            use_container_width=True,
            type="primary" if active_page == "about" else "secondary",
        ):

            if active_page != "about":
                st.switch_page("pages/1_About.py")


    with col3:

        if st.button(
            "💬  Feedback",
            use_container_width=True,
            type="primary" if active_page == "feedback" else "secondary",
        ):

            if active_page != "feedback":
                st.switch_page("pages/2_Feedback.py")


    st.markdown(
        """
        <div style="
            height:1px;
            background:rgba(148,163,184,0.18);
            margin:0 0 25px 0;
        "></div>
        """,
        unsafe_allow_html=True,
    )