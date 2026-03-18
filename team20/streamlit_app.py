import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="TEAM 20: Environmental Justice in New Mexico — 📊 EJI Visualization",
    page_icon="🌎",
    layout="wide"
)

# ------------------------------
# Hide Streamlit default navigation
# ------------------------------
st.markdown('<style>div[data-testid="stSidebarNav"] {display: none;}</style>', unsafe_allow_html=True)

# ------------------------------
# Sidebar Navigation (FIXED)
# ------------------------------
with st.sidebar:
    st.write("---")

    st.page_link(
        "team20/streamlit_app.py",
        label="EJI Visualization",
        icon="📊"
    )

    st.page_link(
        "team20/1_What_Goes_Into_EJI.py",
        label="What Goes Into EJI",
        icon="📘"
    )

    st.page_link(
        "team20/2_EJI_Scale_and_Categories.py",
        label="EJI Scale & Categories",
        icon="📊"
    )

    st.page_link(
        "team20/3_change_over_years_and_comparison.py",
        label="EJI Metrics Comparison",
        icon="📈"
    )

# ------------------------------
# Title
# ------------------------------
st.title("📊 Environmental Justice Index Visualization (New Mexico)")

st.info("""
**Interpreting the EJI Score:**  
Lower values → lower burden (good)  
Higher values → higher burden (bad)
""")

# ------------------------------
# Sample Data Loader (SAFE)
# ------------------------------
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    try:
        state_df = pd.read_csv(BASE_DIR / "2024EJI_StateAverages_RPL.csv")
        county_df = pd.read_csv(BASE_DIR / "2024EJI_NewMexico_CountyMeans.csv")
        tract_df = pd.read_csv(BASE_DIR / "2024EJI_NM_TRACTS.csv")
        return state_df, county_df, tract_df
    except:
        st.warning("⚠️ Data files missing. Using demo data.")
        demo = pd.DataFrame({
            "State": ["New Mexico"],
            "RPL_EJI": [0.6],
            "RPL_EBM": [0.5],
            "RPL_SVM": [0.7],
            "RPL_HVM": [0.65]
        })
        return demo, demo, demo

state_df, county_df, tract_df = load_data()

# ------------------------------
# Simple Visualization
# ------------------------------
st.subheader("New Mexico Overview")

if "RPL_EJI" in state_df.columns:
    val = state_df.iloc[0]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["EJI", "EBM", "SVM", "HVM"],
        y=[
            val.get("RPL_EJI", 0),
            val.get("RPL_EBM", 0),
            val.get("RPL_SVM", 0),
            val.get("RPL_HVM", 0)
        ]
    ))

    fig.update_layout(
        yaxis=dict(range=[0,1]),
        title="EJI Metrics Overview"
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Footer
# ------------------------------
st.divider()
st.caption("Data Source: CDC Environmental Justice Index")
