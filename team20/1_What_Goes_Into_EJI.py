import streamlit as st

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="TEAM 23: Environmental Justice in New Mexico — 📊 EJI Visualization",
    page_icon="🌎",
    layout="wide"
)

# ------------------------------
# Hide Streamlit's Auto Navigation and Add Custom Title in Logo Spot
# ------------------------------
st.markdown(
    '<style>div[data-testid="stSidebarNav"] {display: none;}</style>',
    unsafe_allow_html=True
)

st.markdown(
    """
<style>
div[data-testid="stLogoSpacer"] {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding-top: 40px;
}

div[data-testid="stLogoSpacer"]::before {
    content: "TEAM 23:";
    font-size: 30px;
    font-weight: bold;
    white-space: nowrap;
    margin-bottom: 5px;
}

div[data-testid="stLogoSpacer"]::after {
    content: "🌎 Environmental Justice in New Mexico";
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: -40px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------
# Sidebar Navigation
# ------------------------------
with st.sidebar:
    st.write("---")
    st.page_link("team20/streamlit_app.py", label="EJI Visualization", icon="📊")
    st.page_link("team20/1_What_Goes_Into_EJI.py", label="What Goes Into EJI", icon="📘")
    st.page_link("team20/2_EJI_Scale_and_Categories.py", label="EJI Scale & Categories", icon="📊")
    st.page_link("team20/3_change_over_years_and_comparison.py", label="EJI Metrics Comparison", icon="📈")

st.title("🧩 What Goes Into the Environmental Justice Index (EJI)?")

st.write("""
The **Environmental Justice Index (EJI)** is composed of multiple indicators that measure **social vulnerability**,
**environmental burden**, and **health vulnerability** across U.S. communities.

This diagram, developed by the **CDC and ATSDR**, illustrates how these indicators are grouped into domains
and modules to calculate the overall Environmental Justice score.
""")

st.image("pictures/EJIofficialMarkers.png", width='stretch', caption="Source: CDC Environmental Justice Index")
