import fitz

def is_valid_pdf(path):
    try:
        with fitz.open(path) as doc:
            return doc.page_count > 0
    except Exception as e:
        print(f"[!] Invalid PDF: {e}")
        return False

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join([page.get_text() for page in doc])
