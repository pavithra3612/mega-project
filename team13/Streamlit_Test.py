import streamlit as st
import requests

# Raw URL for the specific commit of Test.py
RAW_URL = "https://raw.githubusercontent.com/ZHud-max/ENG220-Housing/73bcd84f9ec8c0f360083c5d02c53d4e410a540b/Test.py"

st.title("Show Test.py from GitHub and run interactively")

# Fetch and display the raw code from GitHub
try:
    r = requests.get(RAW_URL, timeout=10)
    r.raise_for_status()
    code = r.text
    st.subheader("Source code (Test.py)")
    st.code(code, language="python")
except Exception as e:
    st.error(f"Could not fetch file from GitHub: {e}")

st.subheader("Interactive version (use this instead of input())")
x = st.number_input("Enter a number", value=0, step=1)
if x < 50:
    st.success("You are under 50")
else:
    st.info("You are over 50")
