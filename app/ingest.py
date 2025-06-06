from sentence_transformers import SentenceTransformer
import faiss, pickle
from app.config import INDEX_PATH, DOCS_PATH, EMBEDDING_MODEL_NAME
# Initialize embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)

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
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(chunks, f)
