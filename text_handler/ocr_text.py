from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from a PDF using OCR (Tesseract)
    """
    images = convert_from_path(str(pdf_path))
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text
