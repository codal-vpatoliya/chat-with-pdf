# 🧠 Qwen PDF Question Answering System (Local)

This project lets you upload a PDF, ask questions, and get answers using [Qwen1.5-Chat](https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat) — an open-source large language model.  
Runs **fully offline** on your machine.

---

## 🚀 Setup Instructions
```
python -m venv myenv
source myenv/bin/activate  # On Mac
myenv\Scripts\activate   # On Windows
```

### Install Dependencies
```
pip install -r requirements.txt
```

## 📥 How to Use
1. Add Your PDF
Place your PDF file in the uploads/ folder:
```
uploads/myfile.pdf
```

2. Run the CLI App
```
python cli.py
```

Follow the prompts:
- Enter PDF path (e.g., uploads/myfile.pdf)
- Ask your question

### 💡 Example of Output:
```
=== PDF Q&A with Qwen ===
Enter PDF path (e.g., uploads/myfile.pdf): uploads/terms.pdf
Extracting and indexing text...

Ask a question (or type 'exit'): What is the refund policy?

🧠 Answer: The refund policy states that customers must...
```

## 🌐 API Usage (Frontend Integration)
- Start the FastAPI server:
```
uvicorn app.server:app --reload
```

### API Endpoints:

```
http://127.0.0.1:8000/docs
```

| Method   | Endpoint       | Description              |
| -------- | -------------- | ------------------------ |
| `POST`   | `/upload-pdf/` | Upload a new PDF         |
| `POST`   | `/ask`         | Ask a question about PDF |
| `DELETE` | `/delete-pdf/` | Delete uploaded PDF      |


## 📁 Folder Structure
```
├── app/
│ ├── __init__.py        # model installation on local
│ ├── api.py             # FastAPI routes (upload, ask, delete)
│ ├── config.py          # Model & path configs
│ ├── pdf_reader.py      # PDF text extraction
│ ├── ingest.py          # Chunk + embed + index text
│ ├── qa_engine.py       # Vector search + Qwen answering
│
├── uploads/             # Place your PDFs here
├── vector_store/        # Stores FAISS index + text chunks
│ ├── index.faiss
│ └── docs.pkl
│
├── cli.py               # CLI app to run
├── main.py              # FastAPI server app
├── requirements.txt
└── README.md
```
