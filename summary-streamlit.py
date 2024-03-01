import streamlit as st
import docx2txt
import re
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_document(uploaded_file):
    text = docx2txt.process(uploaded_file)
    # Extract specific section using regex
    pattern = r'(?<=Project Description:).*?(?=Reporting to:)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_text = match.group(0).strip()
        # Summarize the extracted text
        summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
        summary_text = summary[0]['summary_text']
        return summary_text
    else:
        return 'No relevant section found.'

st.title('Upload and Summarize Document')

uploaded_file = st.file_uploader("Choose a .docx file", type="docx")
if uploaded_file is not None:
    summary = summarize_document(uploaded_file)
    st.write("## Summary:")
    st.write(summary)
