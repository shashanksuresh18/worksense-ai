import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("WorkSense AI")

# ---------------- Health check section ----------------
st.write("📡 Checking if API is running...")

try:
    res = requests.get(f"{API_BASE}/")
    if res.status_code == 200:
        st.success("✅ API is running!")
        st.json(res.json())
    else:
        st.error(f"⚠️ API returned status code: {res.status_code}")
except Exception as e:
    st.error(f"❌ Could not reach API: {e}")

st.markdown("---")

# ---------------- Resume upload section ----------------
st.header("📄 Upload your Resume")

uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

if uploaded_file:
    st.info("Sending resume to API for text extraction...")

    # Build the 'files' payload for FastAPI
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }

    try:
        res = requests.post(f"{API_BASE}/upload_resume", files=files)

        if res.status_code == 200:
            data = res.json()
            if "text" in data:
                st.success("✅ Resume processed successfully!")
                st.subheader("Extracted Text:")
                # Use st.text for raw text (better for large chunks)
                st.text(data["text"][:8000])  # show first ~8000 chars
            else:
                st.error(f"API did not return text. Response: {data}")
        else:
            st.error(f"API error: {res.status_code}")
    except Exception as e:
        st.error(f"Request to API failed: {e}")
