from typing import Literal, TypedDict
from pydantic import BaseModel


class DocumentState(BaseModel):
    file_path: str
    document_content: str | None = None
    summary: str | None = None
    feedback: str | None = None
    audit_status: Literal["approved", "rejected"] | None = None
    doc_upload_status: Literal["success", "failed", "pending"] = "pending"
    maximum_iteration: int = 3
    iteration_count: int = 0
    embeddings: list[float] | None = None
    error_message: str | None = None


class AuditResponse(BaseModel):
    feedback: str | None = None
    status: Literal["approved", "rejected"]


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


class IngestionResponse(BaseModel):
    status: Literal["success", "failure", "pending"] | None = None
    message: str
    summary: str | None = None