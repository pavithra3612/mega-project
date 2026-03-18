import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

nav = get_nav_from_toml(".streamlit/pages_sections.toml")

pg = st.navigation(nav)

add_page_title(pg)

if pg.title == "Dashboard Home":
    st.markdown("""
    # ENG220 Combined Project Dashboard

    Welcome to the combined dashboard.

    ## How to Use:
    - Use the sidebar to browse team projects.
    - Some teams may include extra visualization pages.

    ---
    Select a project from the sidebar to get started.
    """)
else:
    pg.run()
