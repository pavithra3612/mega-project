import streamlit as st

# Page config
st.set_page_config(page_title="Credits & Attributions", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
/* Page background */
.stApp {
    background-color: #f0f4f8;
    color: #333333;
    font-family: 'Arial', sans-serif;
}

/* Title styling */
h1 {
    color: #1f77b4;
    text-align: center;
    font-size: 3rem;
    margin-bottom: 0.2em;
}

/* Subheader styling */
h2 {
    color: #ff7f0e;
    text-align: center;
    margin-top: 0.5em;
    margin-bottom: 1em;
}

/* Section headers */
h3 {
    color: #2ca02c;
    margin-top: 1em;
    margin-bottom: 0.5em;
}

/* Card styling for markdown sections */
.credit-card {
    background-color: #ffffff;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

/* Center the gif */
.gif-center {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Main title and subtitle
st.markdown("<h1>Credits & Attributions</h1>", unsafe_allow_html=True)
st.markdown("<h2>Streamlit integration by: Noah Casey</h2>", unsafe_allow_html=True)

# Credit cards
st.markdown('<div class="credit-card">Data points and inspiration from: <a href="https://st.peacedashboard.world" target="_blank">st.peacedashboard.world</a></div>', unsafe_allow_html=True)
st.markdown('<div class="credit-card">Dataset research and justification: Agustin Rodriguez (PM)</div>', unsafe_allow_html=True)
st.markdown('<div class="credit-card">Data cleaning and preprocessing: Jake Miller</div>', unsafe_allow_html=True)
st.markdown('<div class="credit-card">Writing analysis code and producing visualizations: Randall McCoy</div>', unsafe_allow_html=True)
st.markdown('<div class="credit-card">Managing GitHub workflow (branches, commits, merges): Pratik Ojha</div>', unsafe_allow_html=True)
st.markdown('<div class="credit-card">Develop Python scripts for data analysis: Randall McCoy</div>', unsafe_allow_html=True)

# Footer
st.markdown("<h3>Thanks for using our dashboard!</h3>", unsafe_allow_html=True)

# Centered GIF
st.markdown('<div class="gif-center"><img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXN6bGplaHBvMzZldDM5eHAzdWtncmx3azBlZDRtdWhpZjEycGx4ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WRcqyW4t75sTCMrMM0/giphy.gif" width="400"></div>', unsafe_allow_html=True)
