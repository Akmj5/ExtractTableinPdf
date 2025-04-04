import streamlit as st
import pandas as pd
from utils.extractor import extract_tables_from_pdf, convert_tables_to_excel
from utils.validator import validate_table_accuracy

st.title("📄 PDF Table Extractor & Validator")

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])



if uploaded_file:
    st.success("✅ PDF uploaded successfully! Processing...")

    # Extract tables
    tables = extract_tables_from_pdf(uploaded_file)

    # Convert tables to Excel
    excel_file = convert_tables_to_excel(tables)
    st.download_button("📥 Download Excel File", data=excel_file, file_name="extracted_tables.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    if tables:
        st.write(f"🔍 **Extracted {len(tables)} tables from the PDF.**")

        # **Table Preview**
        for i, (sheet_name, table) in enumerate(tables, start=1):
            df = pd.DataFrame(table)
            st.write(f"### 📊 Table {i} Preview ({sheet_name})")
            st.dataframe(df)  # Display table as interactive DataFrame


        # **Validate extracted tables**
        uploaded_file.seek(0)  # Reset file pointer for validation
        validation_scores = validate_table_accuracy(uploaded_file, tables)

        st.write("✅ **Table Extraction Accuracy:**")
        st.table(pd.DataFrame(validation_scores.items(), columns=["Table", "Accuracy (%)"]))
    else:
        st.error("⚠️ No tables found in the PDF.")
