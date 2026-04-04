import os
import shutil
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from git import Repo

from utils.parser import get_code_files, read_file_content
from utils.ai_helper import explain_code_chunk, summarize_repo

app = FastAPI()

# ✅ Serve static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

CLONE_DIR = "repo_clone"


class RepoRequest(BaseModel):
    repo_url: str


def clean_clone_dir():
    if os.path.exists(CLONE_DIR):
        shutil.rmtree(CLONE_DIR)
    os.makedirs(CLONE_DIR, exist_ok=True)


# 🔥 ROOT ROUTE (SERVE YOUR index.html)
@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/analyze")
def analyze_repo(request: RepoRequest):
    repo_url = request.repo_url

    clean_clone_dir()

    try:
        Repo.clone_from(repo_url, CLONE_DIR)
    except Exception as e:
        return {"error": f"Failed to clone repo: {str(e)}"}

    files = get_code_files(CLONE_DIR)

    if not files:
        return {"error": "No valid code files found."}

    file_summaries = []
    results = []

    for file in files[:10]:
        content = read_file_content(file)

        if not content.strip():
            continue

        explanation = explain_code_chunk(content, file)

        file_summaries.append(explanation)

        results.append({
            "file": file,
            "explanation": explanation
        })

    repo_summary = summarize_repo(file_summaries)

    return {
        "repo_summary": repo_summary,
        "files": results
    }


# 🔥 ASK AI (FIXED)
@app.post("/ask")
def ask_question(payload: dict = Body(...)):
    question = payload.get("question")
    context = payload.get("context")

    if not question:
        return {"answer": "Please ask a valid question."}

    if not context:
        return {"answer": "Analyze a repo first."}

    try:
        combined_context = context.get("repo_summary", "") + "\n\n"

        for f in context.get("files", []):
            combined_context += f"{f['file']}:\n{f['explanation']}\n\n"

        prompt = f"""
Answer the question based on the repository context.

Question:
{question}

Context:
{combined_context}

Answer clearly.
"""

        answer = explain_code_chunk(prompt, "repo_question")

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

