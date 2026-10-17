from pathlib import Path
from pypdf import PdfReader
from document_agent_and_auditor.models import DocumentState, AuditResponse
from document_agent_and_auditor.llm_factory import get_llm_factory
from document_agent_and_auditor.prompts import SUMMARIZER_PROMPT, SUMMARIZER_REVISION_PROMPT, AUDITOR_PROMPT

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
    llm = get_llm_factory("medium").get_llm()
    evaluator = llm.with_structured_output(AuditResponse)
    messages = [
        ("system", AUDITOR_PROMPT),
        (
            "human",
            f"Original Document Content:\n{state.document_content}\n\nDraft Summary to Audit:\n{state.summary}",
        ),
    ]
    response: AuditResponse = evaluator.invoke(messages)

    return {
        "status": response.status,
        "feedback": response.feedback,
        "iteration_count": state.iteration_count + 1,
    }

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
    state.summary = summary_result["summary"]

    full_text = (
        state.summary[0]["text"]
        if isinstance(state.summary, list)
        else str(state.summary)
    )
    with open("summary_output.md", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("Full summary saved to summary_output.md!")
    print("Preview:\n" + full_text[:120] + "...\n")

    # After summary_result:
    print("--- 3. Testing Auditor Node ---")
    audit_result = auditor(state)
    print("Audit Status:", audit_result["status"])
    print("Audit Feedback:", audit_result["feedback"])
    print("Iteration Count:", audit_result["iteration_count"])
