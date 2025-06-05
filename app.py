# import os
# import json
# import re
# import streamlit as st
# from utils.pdf_utils import extract_text_from_pdf
# from utils.llm import GroqLLM
# from utils.qa_chain import build_qa_chain, hybrid_answer
# from utils.summary_extractor import extract_summary_fields
# from utils.download_utils import get_download_buttons
#
# st.set_page_config(page_title="Investment Memo Analyzer", layout="centered")
# st.title("📊 Investment Memo Analyzer")
#
# uploaded_file = st.file_uploader("Upload an investment memo (PDF)", type="pdf")
#
# if uploaded_file:
#     text = extract_text_from_pdf(uploaded_file)
#     st.success("✅ PDF Uploaded Successfully")
#
#     groq_llm = GroqLLM()
#     qa_chain = build_qa_chain(text, groq_llm)
#
#     if st.button("📈 Analyze Memo"):
#         with st.spinner("Extracting key fields..."):
#             summary_raw = extract_summary_fields(text, groq_llm)
#             st.text("🔎 Raw LLM output:")
#             st.code(summary_raw)
#
#             match = re.search(r"\{.*\}", summary_raw, re.DOTALL)
#             if match:
#                 try:
#                     clean_json = match.group(0).strip()
#                     if not clean_json.endswith('}'):
#                         clean_json += '}'
#                     summary_dict = json.loads(clean_json)
#                     st.code(summary_dict, language="json")
#                     st.subheader("📝 Summarized Output")
#                     for key, value in summary_dict.items():
#                         st.markdown(f"**{key}**: {', '.join(value) if isinstance(value, list) else value}")
#                     get_download_buttons(summary_dict)
#                 except json.JSONDecodeError as e:
#                     st.error(f"❌ Could not parse JSON: {e}")
#             else:
#                 st.error("❌ No valid JSON object found in LLM output.")
#
#     st.markdown("---")
#     st.subheader("💬 Ask a question about the memo or general finance")
#     query = st.text_input("Enter your question")
#     if st.button("Ask"):
#         label, answer = hybrid_answer(query, qa_chain, groq_llm)
#         st.markdown(f"**{label}**")
#         st.write(answer)
# else:
#     st.info("📄 Please upload an investment memo PDF to begin.")





import os
import json
import re
import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.llm import GroqLLM
from utils.qa_chain import build_qa_chain, hybrid_answer
from utils.summary_extractor import extract_summary_fields
from utils.download_utils import get_download_buttons

st.set_page_config(page_title="Investment Memo Analyzer", layout="centered")
st.title("📊 Investment Memo Analyzer")

uploaded_file = st.file_uploader("Upload an investment memo (PDF)", type="pdf")
summary_dict = None

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF Uploaded Successfully")

    groq_llm = GroqLLM()
    qa_chain = build_qa_chain(text, groq_llm)

    if st.button("📈 Analyze Memo"):
        with st.spinner("Extracting key fields..."):
            summary_raw = extract_summary_fields(text, groq_llm)
            st.text("🔎 Raw LLM output:")
            st.code(summary_raw)

            # Handle wrapped output like ({ ... })
            cleaned_raw = summary_raw.strip()
            if cleaned_raw.startswith("({") and cleaned_raw.endswith("})"):
                cleaned_raw = cleaned_raw[1:-1].strip()

            match = re.search(r"\{[\s\S]*\}", cleaned_raw)
            if match:
                try:
                    clean_json = match.group(0).strip()
                    summary_dict = json.loads(clean_json)
                    st.session_state["memo_summary"] = summary_dict

                except json.JSONDecodeError as e:
                    st.error(f"❌ Could not parse JSON: {e}")
            else:
                st.error("❌ No valid JSON object found in LLM output.")

    if "memo_summary" in st.session_state:
        summary_dict = st.session_state["memo_summary"]
        view_mode = st.radio("📄 Select Output Format", ["JSON", "PDF View"])

        if view_mode == "JSON":
            st.code(summary_dict, language="json")
        elif view_mode == "PDF View":
            st.subheader("📝 Summarized Output")
            for key, value in summary_dict.items():
                st.markdown(f"**{key}**: {', '.join(value) if isinstance(value, list) else value}")

        get_download_buttons(summary_dict)

    st.markdown("---")
    st.subheader("💬 Ask a question ")
    query = st.text_input("Enter your question")
    if st.button("Ask"):
        label, answer = hybrid_answer(query, qa_chain, groq_llm)
        st.markdown(f"**{label}**")
        st.write(answer)
else:
    st.info("📄 Please upload an investment memo PDF to begin.")