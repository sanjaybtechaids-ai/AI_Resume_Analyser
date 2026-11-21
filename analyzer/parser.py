import io
import re
from typing import Tuple, Dict, Any

def extract_text_from_bytes(file_bytes: bytes, filename: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts text from PDF, DOCX, or TXT byte streams.
    Returns: (extracted_text, metadata_dict)
    """
    filename_lower = filename.lower()
    text = ""
    metadata = {"filename": filename, "type": "unknown", "pages": 0, "words": 0}

    if filename_lower.endswith(".pdf"):
        metadata["type"] = "PDF"
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            metadata["pages"] = len(reader.pages)
            page_texts = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    page_texts.append(extracted)
            text = "\n".join(page_texts)
        except Exception as e:
            text = f"Error parsing PDF: {str(e)}"

    elif filename_lower.endswith(".docx"):
        metadata["type"] = "DOCX"
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            paragraphs.append(cell.text.strip())
            text = "\n".join(paragraphs)
            metadata["pages"] = max(1, len(paragraphs) // 10)
        except Exception as e:
            text = f"Error parsing DOCX: {str(e)}"

    elif filename_lower.endswith(".txt"):
        metadata["type"] = "TXT"
        metadata["pages"] = 1
        for encoding in ["utf-8", "latin-1", "cp1252"]:
            try:
                text = file_bytes.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
    else:
        # Fallback to UTF-8 decode
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
            metadata["type"] = "Plain Text"
        except Exception:
            text = ""

    # Clean text
    text = clean_text(text)
    metadata["words"] = len(re.findall(r'\b\w+\b', text))
    return text, metadata

def extract_text_from_file(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """Extracts text from a local file path."""
    with open(file_path, "rb") as f:
        data = f.read()
    return extract_text_from_bytes(data, file_path)

def clean_text(text: str) -> str:
    """Standardizes whitespace, line breaks, and strange characters."""
    if not text:
        return ""
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\r', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
