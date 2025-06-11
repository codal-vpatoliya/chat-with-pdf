import os
from sentence_transformers import SentenceTransformer
import faiss, pickle
from app.config import INDEX_PATH, DOCS_PATH

# Initialize embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Simple text splitter (manual chunking)
def simple_chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_text(text):
    chunks = simple_chunk_text(text)
    embeddings = embedder.encode(chunks)

    # Load or create index
    if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "rb") as f:
            all_chunks = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(embeddings.shape[1])
        all_chunks = []

    # Add new data
    index.add(embeddings)
    all_chunks.extend(chunks)

    # Save back
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)
