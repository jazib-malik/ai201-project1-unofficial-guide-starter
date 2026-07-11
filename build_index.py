import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("chunks.json")
DB_DIR = "chroma_db"
COLLECTION = "unofficial_guide"


def main():
    chunks = json.loads(CHUNKS_FILE.read_text())
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([c["text"] for c in chunks], show_progress_bar=True)

    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=[c["id"] for c in chunks],
        embeddings=embeddings.tolist(),
        documents=[c["text"] for c in chunks],
        metadatas=[
            {"source": c["source"], "title": c["title"], "url": c["url"], "position": c["position"]}
            for c in chunks
        ],
    )
    print(f"indexed {collection.count()} chunks into {DB_DIR}/{COLLECTION}")


if __name__ == "__main__":
    main()
