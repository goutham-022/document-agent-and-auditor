from document_agent_and_auditor.prompts import RAG_QA_PROMPT
from document_agent_and_auditor.llm_factory import get_llm_factory
from document_agent_and_auditor.db import retrieve_relevant_documents
from document_agent_and_auditor.embedding_factory import get_embeddings_factory
from document_agent_and_auditor.models import QueryResponse

async def answer_document_query(
    question: str,
    top_k: int = 3,
    distance_threshold: float = 0.6
) -> QueryResponse:
    embedding_generator = get_embeddings_factory("gemini")
    user_query_embeddings = embedding_generator.get_embeddings().embed_query(question)
    documents = await retrieve_relevant_documents(user_query_embeddings, top_k, distance_threshold)
    if not documents:
        return  QueryResponse(
            answer="Based on the available documents, I do not have sufficient information to answer this question.",
            sources=[]
        )
    context = "\n\n".join([f"Source: {doc.file_path}\n{doc.summary}" for doc in documents])
    # print("context->", context[:200])
    rag_prompt_with_context = RAG_QA_PROMPT.format(context=context, question=question)
    messages = [
        ("human", rag_prompt_with_context),
    ]
    llm = get_llm_factory("low").get_llm()
    response = llm.invoke(messages)
    
    # Handle both raw string or list of content blocks
    if isinstance(response.content, list):
        # Extract the text from each block
        answer_text = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in response.content])
    else:
        answer_text = str(response.content)
    return QueryResponse(
        answer=answer_text,
        sources=[doc.file_path for doc in documents]
    )



if __name__ == "__main__":
    import asyncio
    res = asyncio.run(answer_document_query("What is the first movie of dr.rajkumar"))
    print("\n--- RAG Response ---")
    print("Answer:\n", res)
