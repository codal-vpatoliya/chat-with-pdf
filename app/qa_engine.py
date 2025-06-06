# app/qa_engine.py

import torch
import pickle
import faiss
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from langchain_community.llms import HuggingFacePipeline
from sentence_transformers import SentenceTransformer
from app.config import QWEN_MODEL_NAME, EMBEDDING_MODEL_NAME, INDEX_PATH, DOCS_PATH

# Setup embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Load context docs + index
def get_context(question, k=3):
    with open(DOCS_PATH, "rb") as f:
        docs = pickle.load(f)
    index = faiss.read_index(INDEX_PATH)
    q_vector = embedder.encode([question])
    _, I = index.search(q_vector, k)
    return "\n\n".join([docs[i] for i in I[0]])

# Setup Qwen model with 4-bit quantization
def load_qwen_pipeline():
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    tokenizer = AutoTokenizer.from_pretrained(QWEN_MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        QWEN_MODEL_NAME,
        quantization_config=quantization_config,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True,
        low_cpu_mem_usage=True
    )

    generation_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1
    )

    return HuggingFacePipeline(pipeline=generation_pipeline)

qwen_pipeline = load_qwen_pipeline()

def answer_question(question):
    context = get_context(question)
    prompt = f"<|user|>\nBased on the following content, answer the question:\n\n{context}\n\nQuestion: {question}<|end|>\n<|assistant|>"
    return qwen_pipeline(prompt)
