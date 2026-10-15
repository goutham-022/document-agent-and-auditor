from pathlib import Path
from pypdf import PdfReader
from src.document_agent_and_auditor.state import DocumentState

def parser(state: DocumentState) -> dict:
    file_path = state.file_path
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif path.suffix.lower() in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
    return {"document_content": text}

def summarizer(state: DocumentState) -> dict:
    pass
    
def auditor(state: DocumentState) -> dict:
    pass

def human_reviewer(state: DocumentState) -> dict:
    pass

def db_writer(state: DocumentState) -> dict:
    pass