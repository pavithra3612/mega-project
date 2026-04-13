import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

# -----------------------------
# Navigation setup
# -----------------------------
nav = get_nav_from_toml(".streamlit/pages_sections.toml")
pg = st.navigation(nav)
add_page_title(pg)

# -----------------------------
# Home page
# -----------------------------
if pg.title == "Dashboard Home":
    st.markdown(
        """
        <style>
        .hero {
            padding: 2rem 1.5rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #38bdf8 100%);
            color: white;
            margin-bottom: 1.2rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        }
        .hero h1 {
            margin: 0;
            font-size: 2.4rem;
            font-weight: 800;
        }
        .hero p {
            margin-top: 0.6rem;
            font-size: 1.05rem;
            opacity: 0.95;
        }
        .section-card {
            padding: 1rem 1rem 0.8rem 1rem;
            border-radius: 16px;
            border: 1px solid rgba(0,0,0,0.08);
            background: rgba(255,255,255,0.75);
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            min-height: 170px;
        }
        .mini-card {
            padding: 0.8rem 1rem;
            border-radius: 14px;
            background: #f8fafc;
            border: 1px solid rgba(0,0,0,0.06);
            margin-bottom: 0.8rem;
        }
        .people-card {
            padding: 1rem 1rem 0.8rem 1rem;
            border-radius: 16px;
            border: 1px solid rgba(0,0,0,0.08);
            background: #f8fafc;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .footer-note {
            text-align: center;
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero">
            <h1>🎓 2025 ENG 220 Dashboard</h1>
            <p>
                A unified space for team projects, interactive visualizations, data exploration,
                and presentation-ready insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Welcome to the 2025 ENG 220 Combined Project Dashboard. "
        "Use the sidebar to open team projects and explore their analyses."
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Teams", "20")
    with m2:
        st.metric("Projects", "20+")
    with m3:
        st.metric("Visualizations", "50+")
    with m4:
        st.metric("Topics", "10+")

    st.divider()

    # -----------------------------
    # Professor and TAs section
    # -----------------------------
    st.markdown('<div class="people-card">', unsafe_allow_html=True)
    st.subheader("Course Team")
    st.markdown("### Professor: Dr. Ramiro Jordan")
    st.markdown("#### Teaching Assistants")
    st.markdown(
        """
        - Sri Teja Sudunagunta
        - Pavithra Ravipati
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

    left, mid, right = st.columns([1.2, 1.2, 1])

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("How to Use")
        st.markdown(
            """
            1. Choose a team from the sidebar  
            2. Explore dashboards and extra pages  
            3. Interact with filters, charts, and maps  
            4. Compare findings across projects
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with mid:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Featured Topics")
        st.markdown(
            """
            - Environmental Justice  
            - AQI and Air Quality  
            - Climate Change  
            - Housing and Economics  
            - CO₂ and Emissions  
            - Gun Violence and Public Safety  
            - Infrastructure and Public Data
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="mini-card">', unsafe_allow_html=True)
        st.success("Select a team from the sidebar to get started.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="mini-card">', unsafe_allow_html=True)
        st.write("Some teams include additional visualization pages.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="mini-card">', unsafe_allow_html=True)
        st.write("Built for exploration, comparison, and presentation.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    st.subheader("Project Snapshot")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            **What makes this dashboard useful**
            - Centralized access to all team work
            - Consistent navigation across projects
            - Interactive charts, maps, and tables
            - Deployment-ready presentation format
            """
        )

    with c2:
        st.markdown(
            """
            **Recommended flow**
            - Start with the team overview page
            - Open extra pages where available
            - Use filters to narrow analysis
            - Return to the home page to move across topics
            """
        )

    st.markdown(
        '<div class="footer-note">2025 ENG 220 Combined Dashboard • Built with Streamlit</div>',
        unsafe_allow_html=True,
    )

else:
    pg.run()
