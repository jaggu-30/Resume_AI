from io import BytesIO

from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    """
    Extract text from all pages of a PDF resume.
    """
    reader = PdfReader(file)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_text_from_docx(file):
    """
    Extract text from all paragraphs of a DOCX resume.
    """
    document = Document(file)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_resume_text(file):
    """
    Detect the uploaded file type and extract its text.
    Supports PDF and DOCX.
    """

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload a PDF or DOCX file."
        )