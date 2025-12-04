import pytesseract
from docx2pdf import convert
from pdf2image import convert_from_path
import os
from pypdf import PdfReader
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path, file_type):

    ext = file_type.lower()
    print(f"extension {ext}")

    # ----------------------------------------
    # PDF HANDLING
    # ----------------------------------------
    if "pdf" in ext:
        try:
            # 1) Try normal PDF text extraction
            # reader = PdfReader(file_path)
            # full_text = ""

            # for page in reader.pages:
            #     text = page.extract_text()
            #     if text:
            #         full_text += text + "\n"

            # if full_text.strip():       # If text was found
            #     print("✔ Extracted text using PDFReader")
            #     return full_text

            # # 2) Fallback to OCR (image PDFs)
            # print("❌ PDFReader failed → Using OCR fallback")
            images = convert_from_path(file_path)

            ocr_text = ""
            for img in images:
                text = pytesseract.image_to_string(img)
                ocr_text += text + "\n"

            return ocr_text

        except Exception as e:
            print("PDF error:", e)
            return None

    # ----------------------------------------
    # IMAGE HANDLING
    # ----------------------------------------
    elif ext in ["jpeg", "jpg", "png"]:
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            print("Image OCR error:", e)
            return None

    # ----------------------------------------
    # DOCX HANDLING
    # ----------------------------------------
    elif "docx" in ext or "document" in ext:
        try:

            # Because the word document contains too many tables and paragraphs its hard to extract text from them
            # So we convert it to pdf and then to image and extract text using ocr tesseract
            # Step 1: convert to pdf
            temp_pdf = "temp_extracted.pdf"
            convert(file_path, temp_pdf)

            # Step 2: convert PDF pages to images
            images = convert_from_path(temp_pdf)

            # Step 3: OCR
            full_text = ""
            for img in images:
                text = pytesseract.image_to_string(img)
                full_text += text + "\n"

            # cleanup
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
            return full_text
        except Exception as e:
            print("DOCX extract error:", e)
            return None

    else:
        print("Unsupported file")
        return None
