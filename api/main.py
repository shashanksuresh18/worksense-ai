from fastapi import FastAPI, File, UploadFile
from pypdf import PdfReader

app = FastAPI()


# ---- Health check endpoint ----
@app.get("/")
def home():
    return {"status": "ok", "message": "WorkSense API is running!"}


# ---- Resume upload & PDF parsing ----
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF resume and returns extracted text.
    """
    try:
        # FastAPI gives us a SpooledTemporaryFile via file.file
        pdf_reader = PdfReader(file.file)

        text = ""
        for page in pdf_reader.pages:
            # Some pages may return None, so use `or ""`
            text += (page.extract_text() or "") + "\n"

        return {"text": text}
    except Exception as e:
        # In a real app you'd log this; for now just return the error
        return {"error": str(e)}
