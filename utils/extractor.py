import fitz  # pymupdf
import pandas as pd
import re
from io import BytesIO


def clean_text(text):
    """ Remove non-printable characters from extracted text """
    return re.sub(r'[^\x20-\x7E]', '', text)  # Keep only printable ASCII characters


def extract_tables_from_pdf(pdf_file):
    """ Extract tables as structured text from a system-generated PDF """
    tables_data = []

    try:
        pdf_bytes = pdf_file.read()
        if not pdf_bytes:
            raise ValueError("Uploaded file is empty.")

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text")  # Extract text, ignore images
            lines = [[clean_text(cell) for cell in line.strip().split()] for line in text.split("\n") if line.strip()]

            if lines:
                tables_data.append((f"Page_{page_number}", lines))

    except Exception as e:
        print(f"Error while processing PDF: {e}")

    return tables_data


def convert_tables_to_excel(tables_data):
    """ Convert extracted tables to an Excel file """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, table in tables_data:
            df = pd.DataFrame(table)
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False, header=False)

    output.seek(0)
    return output
