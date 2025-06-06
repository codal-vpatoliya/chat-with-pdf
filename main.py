from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="PDF Q&A API",
    description="Ask questions based on your uploaded documents",
    version="1.0.0"
)

app.include_router(router)
