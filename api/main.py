import os
from fastapi import FastAPI, File, UploadFile, Form
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env (including OPENAI_API_KEY)
load_dotenv()

app = FastAPI()

# OpenAI client (uses OPENAI_API_KEY from environment)
client = OpenAI()

# --- Simple keyword list for skill detection ---
SKILL_KEYWORDS = [
    "python", "sql", "pandas", "numpy", "pyspark", "aws", "azure", "gcp",
    "fastapi", "django", "flask", "machine learning", "deep learning",
    "llm", "large language model", "rag", "data engineering",
    "data science", "power bi", "tableau", "docker", "kubernetes",
]

# --- Very simple role templates for gap analysis ---
ROLE_TEMPLATES = {
    "Founding Engineer": [
        "python", "fastapi", "sql", "aws", "azure", "docker",
        "data engineering", "machine learning",
    ],
    "Applied AI Engineer": [
        "python", "llm", "large language model", "rag",
        "machine learning", "data science", "aws", "pyspark",
    ],
}


def extract_skills_from_text(text: str):
    """Very simple keyword-based skill extractor."""
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.append(skill)
    return sorted(set(found))


def compute_missing_skills(skills, target_role: str):
    """Compare detected skills with what the role template expects."""
    required = set(ROLE_TEMPLATES.get(target_role, []))
    have = set(skills)
    missing = sorted(required - have)
    return list(missing)


def generate_ai_advice(text: str, skills, missing_skills, target_role: str) -> str:
    """
    Uses OpenAI to generate a short, focused career summary and next steps.
    Keeps prompt small to control cost.
    """
    # keep resume snippet small to save tokens
    snippet = text[:1500]

    prompt = f"""
You are a senior hiring manager for a {target_role} role at a fast-moving AI startup.

Candidate resume snippet:
\"\"\"{snippet}\"\"\"

Detected skills: {skills}
Missing skills for this role: {missing_skills}

1. Write a short 3–4 sentence summary explaining how strong this candidate is for a {target_role} role.
2. Then give a bullet list of 3–5 very concrete next steps they should take in the next 1–2 months to become an even stronger fit.
Keep it honest but encouraging. Do NOT repeat the resume, just synthesize.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        # In case of API failure, fall back gracefully
        return f"Could not generate AI advice: {e}"


# ---- Health check endpoint ----
@app.get("/")
def home():
    return {"status": "ok", "message": "WorkSense API is running!"}


# ---- Resume upload & analysis ----
@app.post("/upload_resume")
async def upload_resume(
    target_role: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Accepts a PDF resume + target role and returns:
    - extracted text
    - detected skills
    - missing skills for that role
    - AI-written summary and next steps
    """
    try:
        pdf_reader = PdfReader(file.file)

        text = ""
        for page in pdf_reader.pages:
            text += (page.extract_text() or "") + "\n"

        skills = extract_skills_from_text(text)
        missing = compute_missing_skills(skills, target_role)
        advice = generate_ai_advice(text, skills, missing, target_role)

        return {
            "text": text,
            "skills": skills,
            "target_role": target_role,
            "missing_skills": missing,
            "advice": advice,
        }
    except Exception as e:
        return {"error": str(e)}
