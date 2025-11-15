import streamlit as st
import requests

st.title("WorkSense AI")

st.write("📡 Checking if API is running...")

try:
    res = requests.get("http://127.0.0.1:8000/")
    if res.status_code == 200:
        st.success("✅ API is running!")
        st.json(res.json())
    else:
        st.error(f"⚠️ API returned status code: {res.status_code}")
except Exception as e:
    st.error(f"❌ Could not reach API: {e}")
