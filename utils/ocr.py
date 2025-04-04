import pytesseract
import fitz  # PyMuPDF

# Set Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def perform_ocr(pdf_file):
    """ Extracts text from a scanned PDF using OCR without converting it to images. """
    text = []
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text.append(pytesseract.image_to_string(page.get_pixmap()))
    except Exception as e:
        return f"⚠ OCR Extraction Failed: {e}"

    return "\n".join(text)
