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

2. Run the App
```
python main.py
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

## 📁 Folder Structure
```
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
```
