import pickle, faiss
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from sentence_transformers import SentenceTransformer
from app.config import MODEL_ID, INDEX_PATH, DOCS_PATH, EMBEDDING_MODEL

# Load models
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True).eval()
embedder = SentenceTransformer(EMBEDDING_MODEL)

def get_context(question, k=3):
    with open(DOCS_PATH, "rb") as f:
        docs = pickle.load(f)
    index = faiss.read_index(INDEX_PATH)
    q_vector = embedder.encode([question])
    _, I = index.search(q_vector, k)
    return "\n\n".join([docs[i] for i in I[0]])

def answer_question(question):
    context = get_context(question)
    prompt = f"<|user|>\nBased on the following content, answer the question:\n\n{context}\n\nQuestion: {question}<|end|>\n<|assistant|>"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=300, do_sample=True)
    return tokenizer.decode(output[0], skip_special_tokens=True).split("<|assistant|>")[-1].strip()
