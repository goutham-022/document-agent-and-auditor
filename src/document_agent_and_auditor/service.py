import os
import uuid
from fastapi import UploadFile
from document_agent_and_auditor.models import DocumentState, IngestionResponse
from document_agent_and_auditor.graph import app as agent_app

ALLOWED_EXTENSIONS = {".txt", ".pdf", ".md"}

async def _save_the_file(file: UploadFile) -> str:
    os.makedirs("data/uploads", exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    contents = await file.read()
    file_path = f"data/uploads/{unique_filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    return file_path


async def ingest_document(file: UploadFile) -> IngestionResponse:
    # 1. API Guardrail: Validate extension before saving or running graph
    file_ext = os.path.splitext(file.filename or "")[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return IngestionResponse(
            status="failure",
            message=f"Unsupported file format '{file_ext}'. Allowed formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            summary=None,
        )

    try:
        file_path = await _save_the_file(file)
        agent_state = DocumentState(file_path=file_path)
        response = await agent_app.ainvoke(agent_state)

        if response.get("doc_upload_status") == "success":
            return IngestionResponse(
                status="success",
                message="Document successfully processed, audited, and indexed into database.",
                summary=response.get("summary"),
            )
        elif response.get("doc_upload_status") == "failed":
            error_reason = response.get("error_message") or "Unknown error"
            return IngestionResponse(
                status="failure",
                message=f"Document processing failed: {error_reason}",
                summary=response.get("summary"),
            )
        else:
            return IngestionResponse(
                status="pending",
                message=f"Document processing pending. Audit status: {response.get('audit_status')}",
                summary=response.get("summary"),
            )
    except Exception as e:
        return IngestionResponse(
            status="failure",
            message=f"System error during document ingestion: {str(e)}",
            summary=None,
        )


