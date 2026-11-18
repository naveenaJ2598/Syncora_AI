
from pypdf import PdfReader


def extract_text(file):
    file_name = file.filename.lower()

    if file_name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text.strip()

    elif file_name.endswith(".txt"):
        return file.read().decode("utf-8").strip()

    else:
        raise ValueError("Only PDF and TXT files are supported.")
