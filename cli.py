from app.pdf_reader import extract_text
from app.ingest import ingest_text
from app.qa_engine import answer_question

def main():
    print("=== PDF Q&A with Qwen ===")
    pdf_path = input("Enter PDF path (e.g., uploads/sample.pdf): ").strip()
    text = extract_text(pdf_path)
    print("Extracting and indexing text...")
    ingest_text(text)

    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == 'exit':
            break
        answer = answer_question(q)
        print(f"\n🧠 Answer: {answer}")

if __name__ == "__main__":
    main()
