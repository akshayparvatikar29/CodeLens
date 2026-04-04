import os

# ✅ Supported file types (UPDATED)
VALID_EXTENSIONS = [
    ".py", ".js", ".ts", ".java", ".go",
    ".rb",        # ✅ CRITICAL FIX (your repo)
    ".cpp", ".c", ".cs",
    ".html", ".css",
    ".json", ".yml", ".yaml"
]

# ✅ Ignore junk folders
EXCLUDE_DIRS = [".git", "__pycache__", "node_modules", "venv"]


def get_code_files(repo_path):
    code_files = []

    for root, dirs, files in os.walk(repo_path):
        # remove excluded dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if any(file.endswith(ext) for ext in VALID_EXTENSIONS):
                full_path = os.path.join(root, file)
                code_files.append(full_path)

    return code_files


def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""
