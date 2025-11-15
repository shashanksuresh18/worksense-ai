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

# ---------------- Target role selection ----------------
st.header("🎯 Choose your target role")

target_role = st.selectbox(
    "Target Role",
    ["Founding Engineer", "Applied AI Engineer"],
    index=0,
)

st.markdown("---")

# ---------------- Resume upload section ----------------
st.header("📄 Upload your Resume")

uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

if uploaded_file:
    st.info(f"Sending resume to API for analysis as '{target_role}'...")

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }
    data = {"target_role": target_role}

    try:
        res = requests.post(f"{API_BASE}/upload_resume", files=files, data=data)

        if res.status_code == 200:
            data = res.json()

            if "text" in data:
                st.success("✅ Resume processed successfully!")

                skills = data.get("skills", [])
                missing = data.get("missing_skills", [])
                advice = data.get("advice", "")

                st.subheader("Detected Skills:")
                if skills:
                    st.write(", ".join(skills))
                else:
                    st.warning("No skills detected (keyword list is still simple).")

                st.subheader(f"Missing Skills for {target_role}:")
                if missing:
                    st.write(", ".join(missing))
                else:
                    st.success("You already match this role's skill template! 🎉")

                if advice:
                    st.subheader("💡 AI Career Summary & Next Steps")
                    st.markdown(advice)

                st.subheader("Extracted Text (first part):")
                st.text(data["text"][:8000])
            else:
                st.error(f"API did not return text. Response: {data}")
        else:
            st.error(f"API error: {res.status_code}")
    except Exception as e:
        st.error(f"Request to API failed: {e}")
