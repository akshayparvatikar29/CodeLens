import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in environment")

client = Groq(api_key=api_key)

# ✅ Stable models (fallback support)
MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile"
]


# 🔥 Core Groq caller (safe + fallback)
def call_groq(messages, max_tokens=300):
    last_error = None

    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content

            if content and content.strip():
                return content.strip()

        except Exception as e:
            last_error = str(e)
            continue

    return f"AI failed: {last_error}"


# ✅ FILE EXPLANATION (CLEAN BULLETS)
def explain_code_chunk(code, file_path):
    messages = [
        {
            "role": "system",
            "content": "You are a senior software engineer. Be concise and structured."
        },
        {
            "role": "user",
            "content": f"""
Explain this file in EXACT format:

- Purpose:
- Key Function:
- Connections:
- API/Logic:

File: {file_path}

IMPORTANT:
- Use bullet points starting with "-"
- Maximum 4 bullets
- Keep it short and clean

Code:
{code}
"""
        }
    ]

    return call_groq(messages, max_tokens=300)
# ✅ REPO SUMMARY (STRICT 2 SENTENCES)
def summarize_repo(file_summaries):
    combined = "\n\n".join(file_summaries[:5])

    messages = [
        {
            "role": "system",
            "content": "You summarize codebases in exactly 2 clear sentences."
        },
        {
            "role": "user",
            "content": f"""
Summarize this repository in EXACTLY 2 sentences.

Rules:
- No bullet points
- No extra explanation
- No formatting
- Just 2 clean sentences

Context:
{combined}
"""
        }
    ]

    return call_groq(messages, max_tokens=120)

