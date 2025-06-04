# 🧠 Qwen PDF Question Answering System (Local)

This project lets you upload a PDF, ask questions, and get answers using [Qwen1.5-Chat](https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat) — an open-source large language model.  
Runs **fully offline** on your machine.

---

## 📁 Folder Structure

├── app/
│ ├── config.py # Model & path configs
│ ├── pdf_reader.py # PDF text extraction
│ ├── ingest.py # Chunk + embed + index text
│ ├── qa_engine.py # Vector search + Qwen answering
│
├── uploads/ # Place your PDFs here
├── vector_store/ # Stores FAISS index + text chunks
│ ├── index.faiss
│ └── docs.pkl
│
├── main.py # CLI app to run
├── requirements.txt
└── README.md


---

## 🚀 Setup Instructions

### python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
