import streamlit as st

st.title("All Teams Dashboard")
st.write("This page lists all team projects included in the repository.")

teams = [
    ("Team 1", "team1", [
        "DashboardFrontPage.py",
        "1_Custom Histogram.py",
        "2_Powerful Data Parser.py",
        "3_Data Visualizer.py",
        "4_Credits & Attributions.py",
    ]),
    ("Team 3", "team3", ["app.py"]),
    ("Team 5", "team5", ["streamlit_app.py"]),
    ("Team 6", "teram6", ["streamlit.py"]),
    ("Team 7", "team7", ["app.py"]),
    ("Team 8", "team8", ["streamlit_app.py"]),
    ("Team 9", "team9", ["streamlit_app.py"]),
    ("Team 10", "team10", ["streamlit_app.py"]),
    ("Team 11", "team11", ["app.py"]),
    ("Team 12", "team12", ["app.py"]),
    ("Team 13", "team13", ["App.py", "California_Housing_(Streamlit).py", "Streamlit_Test.py"]),
    ("Team 14", "team14", ["app.py"]),
    ("Team 15", "team15", ["app.py"]),
    ("Team 16", "team16", ["alejandro_water_data_analysis.py"]),
    ("Team 17", "team17", ["app.py"]),
    ("Team 18", "team18", ["streamlit_app.py", "StockCrash.py"]),
    ("Team 19", "team19", ["app.py"]),
    ("Team 20", "team20", [
        "streamlit_app.py",
        "1_What_Goes_Into_EJI.py",
        "2_EJI_Scale_and_Categories.py",
        "3_change_over_years_and_comparison.py",
    ]),
]

for team_name, folder, files in teams:
    st.subheader(team_name)
    st.write(f"Folder: `{folder}`")
    st.write("Files:")
    for f in files:
        st.code(f"{folder}/{f}")
