from fastapi import APIRouter, UploadFile
from document_agent_and_auditor.models import QueryRequest, QueryResponse, IngestionResponse
from document_agent_and_auditor.rag import answer_document_query
from document_agent_and_auditor.service import ingest_document

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile) -> IngestionResponse:
    return await ingest_document(file)

@router.post("/query")
async def query_document(query: QueryRequest) -> QueryResponse:
    response = await answer_document_query(query.question)
    return response