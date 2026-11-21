"""Clone/read a repo, chunk files, embed with Ollama, store in ChromaDB."""
import sys
from pathlib import Path

import chromadb
import ollama
from git import Repo

from app import config


def clone_or_path(source: str) -> Path:
    if source.startswith("http"):
        name = source.rstrip("/").split("/")[-1].removesuffix(".git")
        dest = config.REPOS_DIR / name
        if not dest.exists():
            Repo.clone_from(source, dest, depth=1)
        return dest
    return Path(source)


def iter_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in config.CODE_EXTENSIONS and not (set(p.parts) & config.IGNORE_DIRS):
            yield p


def chunk_file(path: Path, root: Path):
    lines = path.read_text(errors="ignore").splitlines()
    step = config.CHUNK_LINES - config.CHUNK_OVERLAP
    for start in range(0, max(len(lines), 1), step):
        body = "\n".join(lines[start : start + config.CHUNK_LINES])
        if body.strip():
            yield {
                "text": body,
                "file": str(path.relative_to(root)),
                "start": start + 1,
                "end": min(start + config.CHUNK_LINES, len(lines)),
            }


def build_index(source: str, collection_name: str = "repo"):
    root = clone_or_path(source)
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    col = client.create_collection(collection_name)
    n = 0
    for f in iter_files(root):
        for c in chunk_file(f, root):
            emb = ollama.embed(model=config.EMBED_MODEL, input=c["text"])["embeddings"][0]
            col.add(
                ids=[f"{c['file']}:{c['start']}"],
                documents=[c["text"]],
                embeddings=[emb],
                metadatas=[{"file": c["file"], "start": c["start"], "end": c["end"]}],
            )
            n += 1
    print(f"Indexed {n} chunks from {root}")


if __name__ == "__main__":
    build_index(sys.argv[1])
