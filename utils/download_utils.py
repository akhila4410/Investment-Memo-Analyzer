import streamlit as st
from fpdf import FPDF
import tempfile
import json

def get_download_buttons(parsed):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in parsed.items():
        line = f"{key}: {', '.join(value) if isinstance(value, list) else value}"
        pdf.multi_cell(0, 10, line)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        tmpfile.seek(0)
        st.download_button("📄 Download Summary (PDF)", tmpfile.read(), file_name="memo_summary.pdf")

    # Download JSON
    json_bytes = json.dumps(parsed, indent=2).encode("utf-8")
    st.download_button("📥 Download Summary (JSON)", json_bytes, file_name="memo_summary.json")

    # Download TXT
    txt_lines = [f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k, v in parsed.items()]
    txt_content = "\n\n".join(txt_lines).encode("utf-8")
    st.download_button("📄 Download Summary (Text)", txt_content, file_name="memo_summary.txt")
