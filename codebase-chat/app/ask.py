"""Retrieve relevant chunks and answer with citations using a local Ollama model."""
import sys

import chromadb
import ollama

from app import config

PROMPT = """You are a code assistant. Answer ONLY using the context below.
Cite sources as [file:start-end]. If the context is insufficient, say "I don't know".

Context:
{context}

Question: {question}"""


def retrieve(question: str, collection_name: str = "repo"):
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    col = client.get_collection(collection_name)
    emb = ollama.embed(model=config.EMBED_MODEL, input=question)["embeddings"][0]
    res = col.query(query_embeddings=[emb], n_results=config.TOP_K)
    return list(zip(res["documents"][0], res["metadatas"][0]))


def answer(question: str):
    hits = retrieve(question)
    context = "\n\n".join(
        f"[{m['file']}:{m['start']}-{m['end']}]\n{d}" for d, m in hits
    )
    resp = ollama.chat(
        model=config.LLM_MODEL,
        messages=[{"role": "user", "content": PROMPT.format(context=context, question=question)}],
    )
    return resp["message"]["content"], [m for _, m in hits]


if __name__ == "__main__":
    text, sources = answer(" ".join(sys.argv[1:]))
    print(text)
