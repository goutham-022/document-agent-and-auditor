from pathlib import Path
from pypdf import PdfReader
from document_agent_and_auditor.state import DocumentState
from document_agent_and_auditor.llm_factory import get_llm_factory
from document_agent_and_auditor.prompts import SUMMARIZER_PROMPT, SUMMARIZER_REVISION_PROMPT

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
    llm = get_llm_factory("low").get_llm()
    if not state.feedback:
        messages = [
            ("system", SUMMARIZER_PROMPT),
            ("human", f"Please summarize this document:\n\n{state.document_content}"),
        ]
    else:
        revision_text = SUMMARIZER_REVISION_PROMPT.format(
            document_content=state.document_content,
            previous_summary=state.summary,
            feedback=state.feedback,
        )
        messages = [
            ("human", revision_text),
        ]
    response = llm.invoke(messages)
    return {"summary": response.content}
    
def auditor(state: DocumentState) -> dict:
    pass

def human_reviewer(state: DocumentState) -> dict:
    pass

def db_writer(state: DocumentState) -> dict:
    pass


if __name__ == "__main__":
    print("--- 1. Testing Parser Node ---")
    state = DocumentState(file_path="sample_testing.txt")
    parse_result = parser(state)
    state.document_content = parse_result["document_content"]
    print(f"Parser succeeded! Extracted {len(state.document_content)} characters.")

    print("\n--- 2. Testing Summarizer Node ---")
    summary_result = summarizer(state)
    print("\n=== GENERATED SUMMARY ===")
    print(summary_result["summary"])