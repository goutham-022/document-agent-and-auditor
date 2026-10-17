from typing import Literal, TypedDict
from pydantic import BaseModel


class DocumentState(BaseModel):
    file_path: str
    document_content: str | None = None
    summary: str | None = None
    feedback: str | None = None
    status: Literal["approved", "rejected"] | None = None
    maximum_iteration: int = 3
    iteration_count: int = 0


class AuditResponse(BaseModel):
    feedback: str | None = None
    status: Literal["approved", "rejected"]
    
    
