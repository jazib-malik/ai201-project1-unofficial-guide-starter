import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

DB_DIR = "chroma_db"
COLLECTION = "unofficial_guide"
TOP_K = 5
MAX_DISTANCE = 0.65

SYSTEM_PROMPT = """You answer questions about student life at UC Berkeley using only the excerpts from r/berkeley threads provided below. Rules:
- Use only information that appears in the excerpts. Do not use any outside knowledge about Berkeley or anything else.
- If the excerpts do not contain enough information to answer, reply exactly: "I don't have enough information on that in my documents."
- When you make a claim, mention which thread it came from, for example: according to the thread "Safe to live alone in southside".
- These are student opinions, so present them as what students say, not as verified facts."""

_model = None
_collection = None
_groq = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=DB_DIR)
        _collection = client.get_collection(COLLECTION)
    return _collection


def get_groq():
    global _groq
    if _groq is None:
        _groq = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _groq


def retrieve(question, k=TOP_K):
    embedding = get_model().encode([question])
    result = get_collection().query(query_embeddings=embedding.tolist(), n_results=k)
    hits = []
    for text, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        hits.append({"text": text, "source": meta["source"], "title": meta["title"], "url": meta["url"], "distance": dist})
    return hits


def ask(question, k=TOP_K):
    hits = retrieve(question, k)
    usable = [h for h in hits if h["distance"] <= MAX_DISTANCE]
    if not usable:
        return {
            "answer": "I don't have enough information on that in my documents.",
            "sources": [],
            "hits": hits,
        }
    context = "\n\n---\n\n".join(
        f"Excerpt {i + 1} (from {h['source']}):\n{h['text']}" for i, h in enumerate(usable)
    )
    response = get_groq().chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Excerpts:\n\n{context}\n\nQuestion: {question}"},
        ],
    )
    answer = response.choices[0].message.content
    if "don't have enough information" in answer.lower():
        return {"answer": answer, "sources": [], "hits": usable}
    sources = []
    for h in usable:
        label = f"{h['source']} ({h['url']})"
        if label not in sources:
            sources.append(label)
    return {"answer": answer, "sources": sources, "hits": usable}


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) or "Is it safe to live alone in southside?"
    result = ask(question)
    print(result["answer"])
    print()
    print("Sources:")
    for s in result["sources"]:
        print(f"  - {s}")
