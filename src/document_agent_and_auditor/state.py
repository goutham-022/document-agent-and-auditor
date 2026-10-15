from typing import Literal, TypedDict
from pydantic import BaseModel


class DocumentState(BaseModel):
    file_path: str
    document_content: str | None = None
    summary: str | None = None
    feedback: str | None = None
    status: Literal["approved", "rejected"] | None = None
    iteration_count: int = 0
