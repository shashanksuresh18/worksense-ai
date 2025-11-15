from fastapi import FastAPI, File, UploadFile, Form
from pypdf import PdfReader

app = FastAPI()

# --- simple keyword list for now ---
SKILL_KEYWORDS = [
    "python", "sql", "pandas", "numpy", "pyspark", "aws", "azure", "gcp",
    "fastapi", "django", "flask", "machine learning", "deep learning",
    "llm", "large language model", "rag", "data engineering",
    "data science", "power bi", "tableau", "docker", "kubernetes",
]

# --- very simple role templates ---
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
    """
    try:
        pdf_reader = PdfReader(file.file)

        text = ""
        for page in pdf_reader.pages:
            text += (page.extract_text() or "") + "\n"

        skills = extract_skills_from_text(text)
        missing = compute_missing_skills(skills, target_role)

        return {
            "text": text,
            "skills": skills,
            "target_role": target_role,
            "missing_skills": missing,
        }
    except Exception as e:
        return {"error": str(e)}
