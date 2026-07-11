import html
import json
import re
from pathlib import Path

DOCS_DIR = Path("documents")
CHUNKS_FILE = Path("chunks.json")
MAX_CHUNK_CHARS = 800


def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r"\[([^\]]*)\]\((https?://[^)]+)\)", r"\1", text)
    text = re.sub(r"https?://preview\.redd\.it/\S+", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = text.replace("**", "").replace("\\(", "(").replace("\\)", ")")
    text = re.sub(r"^\[\d+ points\]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"&#x200B;", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_documents():
    docs = []
    for path in sorted(DOCS_DIR.glob("*.txt")):
        raw = path.read_text()
        lines = raw.split("\n")
        title = lines[0].replace("Title: ", "").strip()
        url = lines[1].replace("Source: r/berkeley thread, ", "").strip()
        body = clean_text("\n".join(lines[3:]))
        docs.append({"source": path.name, "title": title, "url": url, "body": body})
    return docs


def split_long_paragraph(para):
    sentences = re.split(r"(?<=[.!?])\s+", para)
    pieces = []
    current = ""
    for s in sentences:
        if current and len(current) + len(s) > MAX_CHUNK_CHARS:
            pieces.append(current.strip())
            current = ""
        current += s + " "
    if current.strip():
        pieces.append(current.strip())
    return pieces


def chunk_document(doc):
    raw_paragraphs = [p.strip() for p in doc["body"].split("\n\n") if p.strip()]
    raw_paragraphs = [p for p in raw_paragraphs if p not in ("Original post:", "Replies from students:")]
    paragraphs = []
    for p in raw_paragraphs:
        if len(p) > MAX_CHUNK_CHARS:
            paragraphs.extend(split_long_paragraph(p))
        else:
            paragraphs.append(p)
    header = f"Thread: {doc['title']}\n"
    chunks = []
    current = []
    current_len = 0
    for para in paragraphs:
        if current and current_len + len(para) > MAX_CHUNK_CHARS:
            chunks.append(header + "\n".join(current))
            current = [current[-1]] if len(current[-1]) < 300 else []
            current_len = sum(len(p) for p in current)
        current.append(para)
        current_len += len(para)
    if current:
        chunks.append(header + "\n".join(current))
    return chunks


def main():
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        for i, text in enumerate(chunk_document(doc)):
            all_chunks.append({
                "id": f"{doc['source']}_{i}",
                "text": text,
                "source": doc["source"],
                "title": doc["title"],
                "url": doc["url"],
                "position": i,
            })
    CHUNKS_FILE.write_text(json.dumps(all_chunks, indent=2))
    print(f"{len(docs)} documents, {len(all_chunks)} chunks written to {CHUNKS_FILE}")


if __name__ == "__main__":
    main()
