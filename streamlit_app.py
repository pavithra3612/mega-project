if pg.title == "Dashboard Home":
    st.markdown("""
    # 🎓 2025 ENG 220 Dashboard
    ### Interactive team projects, visualizations, and data stories in one place.
    """)

    st.info("""
    Welcome to the **2025 ENG 220 Combined Project Dashboard**.

    Use the sidebar to browse team projects, dashboards, and visualization pages.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Teams", "20")

    with col2:
        st.metric("Projects", "20+")

    with col3:
        st.metric("Visualizations", "50+")

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.markdown("""
        ## How to Use
        - Browse team projects from the sidebar  
        - Open dashboards and visualizations  
        - Explore insights, charts, and datasets  
        """)

        st.markdown("""
        ## Featured Topics
        Environmental Justice, AQI, Housing, Climate Change, Gun Violence, CO₂ Analysis, Emissions, and more.
        """)

    with right:
        st.success("Select a team from the sidebar to get started.")
        st.caption("Each team may include extra visualization pages.")

    st.divider()
    st.caption("2025 ENG 220 Combined Dashboard • Built with Streamlit")
