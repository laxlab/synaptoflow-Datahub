import chromadb
import os

# Creates (or reopens) a local vector database saved to disk in ./chroma_db
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("synaptoflow_docs")

def chunk_text(text, chunk_size=800, overlap=150):
    """Split long text into overlapping chunks.
    Overlap matters: without it, an answer that spans a chunk boundary
    gets cut in half and the bot won't find it properly."""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

def ingest_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text)
    ids = [f"{os.path.basename(filepath)}-{i}" for i in range(len(chunks))]
    # No manual embedding step: Chroma turns each chunk into a vector
    # (a list of numbers representing its meaning) with its built-in model.
    # upsert = add new chunks or overwrite old ones, so re-running is safe.
    collection.upsert(documents=chunks, ids=ids)
    print(f"Ingested {len(chunks)} chunks from {filepath}")

if __name__ == "__main__":
    ingest_file("README.md")
