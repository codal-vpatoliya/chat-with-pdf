import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from app.qa_engine import answer_question
from app.pdf_reader import extract_text
from app.ingest import ingest_text
from app.config import INDEX_PATH, DOCS_PATH

router = APIRouter()
UPLOAD_DIR = "uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract and ingest
        text = extract_text(file_path)
        ingest_text(text)

        return {"message": f"{file.filename} uploaded and indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):
    try:
        answer = answer_question(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-pdf")
async def delete_pdf(filename: str = Query(..., description="Name of the PDF file to delete")):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        os.remove(file_path)

        # Optionally clear embeddings and index
        if os.path.exists(INDEX_PATH):
            os.remove(INDEX_PATH)
        if os.path.exists(DOCS_PATH):
            os.remove(DOCS_PATH)

        return {"message": f"{filename} deleted successfully along with its index."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
