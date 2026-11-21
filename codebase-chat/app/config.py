from pathlib import Path

LLM_MODEL = "qwen3:4b"
EMBED_MODEL = "nomic-embed-text"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CHROMA_DIR = DATA_DIR / "chroma"
REPOS_DIR = DATA_DIR / "repos"
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".cpp", ".c", ".h", ".md"}
IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
CHUNK_LINES = 40
CHUNK_OVERLAP = 8
TOP_K = 5
