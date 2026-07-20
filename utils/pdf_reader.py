from typing import BinaryIO

from PyPDF2 import PdfReader


def extract_text_from_pdf(uploaded_file: BinaryIO) -> str:
    """Extract all available text from a PDF uploaded through Streamlit."""
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
