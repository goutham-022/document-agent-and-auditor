import asyncio

from pathlib import Path
from pypdf import PdfReader
from document_agent_and_auditor.models import DocumentState, AuditResponse
from document_agent_and_auditor.llm_factory import get_llm_factory
from document_agent_and_auditor.prompts import SUMMARIZER_PROMPT, SUMMARIZER_REVISION_PROMPT, AUDITOR_PROMPT
from document_agent_and_auditor.embedding_factory import get_embeddings_factory
from document_agent_and_auditor.db import AsyncSessionLocal, DocumentRecord


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
    
    summary_text = (
        response.content[0]["text"]
        if isinstance(response.content, list) and len(response.content) > 0 and isinstance(response.content[0], dict)
        else str(response.content)
    )

    with open("summary_output.md", "w", encoding="utf-8") as f:
        f.write(summary_text)

    return {"summary": summary_text}
    
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
    print(f"\n⚠️ ESCALATION: Document reached maximum iterations ({state.maximum_iteration}) without approval.")
    print(f"Auditor's Last Feedback: {state.feedback}")
    print("*"*50)
    print("👉 Please review the draft in 'summary_output.md' before proceeding.\n")

    decision = input("Admin Decision (approve / reject): ").strip().lower()

    while decision not in ["approve", "reject"]:
        print(f"❌ Invalid decision: {decision}. Please try again.")
        decision = input("Admin Decision (approve / reject): ").strip().lower()

    if decision == "approve":
        return {"status": "approved", "feedback": None}
    else:
        admin_feedback = input("Enter revision instructions for the summarizer: ")
        return {
            "status": "rejected",
            "feedback": admin_feedback,
            "iteration_count": 0,
        }

def embedding_generator(state: DocumentState) -> dict:
    print("\n--- Embedding Generator Node ---")
    embedding_generator = get_embeddings_factory("gemini")
    embeddings = embedding_generator.get_embeddings().embed_query(state.summary)
    return {"embeddings": embeddings}


async def db_writer(state: DocumentState) -> dict:
    print("\n--- DB Writer Node ---")
    print("Saving approved summary to database... (PostgreSQL / pgvector yet to be configured)")
    file_path = state.file_path
    summary = state.summary
    embeddings = state.embeddings

    record = DocumentRecord(
        file_path=file_path,
        summary=summary,
        embedding=embeddings,
        created_by="agent",
    )

    async with AsyncSessionLocal() as session:
        session.add(record)
        await session.commit()
    
    print("Successfully persisted document and vector embedding to PostgreSQL!")
    return {}


if __name__ == "__main__":
    print("--- 1. Testing Parser Node ---")
    state = DocumentState(file_path="sample_testing.txt")
    parse_result = parser(state)
    state.document_content = parse_result["document_content"]
    print(f"Parser succeeded! Extracted {len(state.document_content)} characters.")

    print("\n--- 2. Testing Summarizer Node ---")
    summary_result = summarizer(state)
    state.summary = summary_result["summary"]
    print(f"Summary generated ({len(state.summary)} chars) and saved to summary_output.md!")
    print("Preview:\n" + state.summary[:120] + "...\n")

    # After summary_result:
    print("--- 3. Testing Auditor Node ---")
    audit_result = auditor(state)
    print("Audit Status:", audit_result["status"])
    print("Audit Feedback:", audit_result["feedback"])
    print("Iteration Count:", audit_result["iteration_count"])
