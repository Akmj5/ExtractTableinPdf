import fitz  # pymupdf

def validate_table_accuracy(pdf_file, extracted_tables):
    """ Validate extracted tables by comparing with original PDF text """
    accuracy_scores = {}

    try:
        pdf_bytes = pdf_file.read()
        if not pdf_bytes:
            raise ValueError("Uploaded file is empty.")

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_number, (sheet_name, table) in enumerate(extracted_tables, start=1):
            pdf_text = doc[page_number - 1].get_text("text")  # Extract page text
            extracted_text = "\n".join([" ".join(row) for row in table])

            # Simple accuracy check: Percentage of table words in PDF text
            match_count = sum(1 for word in extracted_text.split() if word in pdf_text)
            total_words = len(extracted_text.split())

            accuracy_scores[sheet_name] = round((match_count / total_words) * 100, 2) if total_words else 0

    except Exception as e:
        print(f"Error in validation: {e}")

    return accuracy_scores
