# WorkSense AI

**WorkSense AI** is an AI-powered career and work intelligence engine that helps you:

* Upload your resume or work logs
* Extract your skills automatically
* Discover your strengths and gaps
* Compare yourself with real job role templates
* Generate a clean AI-created portfolio
* Prepare for interviews

This project is built to demonstrate full end-to-end AI product thinking for Founding Engineer and Applied AI Engineer roles.

---

## 🚀 Features (MVP)

* Resume upload (PDF)
* Resume text extraction
* Local embeddings using SentenceTransformers
* Basic skill extraction (keyword + AI powered)
* Gap analysis for target roles
* Portfolio generator (Markdown)
* Streamlit UI + FastAPI backend

---

## 🧠 Tech Stack

**Backend:** FastAPI (Python)
**Frontend:** Streamlit
**Embeddings:** sentence-transformers (MiniLM)
**Vector DB:** ChromaDB (local)
**LLM:** OpenAI GPT-4o-mini (optional)
**Database:** SQLite (minimal)

---

## 📁 Project Structure

```
worksense-ai/
│
├── api/
│   └── main.py
│
├── ui/
│   └── app.py
│
├── docs/
│   └── architecture.md
│
└── requirements.txt (coming soon)
```

---

## 🏃 How to Run Locally

1. Clone the repo:

```
git clone https://github.com/shashanksuresh18/worksense-ai.git
cd worksense-ai
```

2. Create a virtual environment and activate:

```
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies (after requirements.txt is added):

```
pip install -r requirements.txt
```

4. Run Backend:

```
uvicorn api.main:app --reload
```

5. Run UI:

```
streamlit run ui/app.py
```

---

## 🎯 Goals

This project is intentionally minimal but demonstrates:

* Fast 0→1 execution
* End-to-end AI product building
* Real engineering + product thinking
* Domain alignment with Hiring AI / Work AI startups like Jack & Jill and Shram.ai

---

## 📌 Status

This is **v0.1** — the foundation is set up.
Updates will be added in small commits to show consistent progress.

---

## 📧 Contact

If you're reviewing this repo for hiring purposes:
Feel free to reach out at **[shashanksuresh018@gmail.com](mailto:shashanksuresh018@gmail.com)**.
