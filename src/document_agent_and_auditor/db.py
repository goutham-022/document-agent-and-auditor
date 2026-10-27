import uuid
import asyncio
from datetime import datetime, timezone
from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, String, Text, func, text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from document_agent_and_auditor.utils.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class DocumentRecord(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
        nullable=True,
    )
    created_by: Mapped[str] = mapped_column(
        String(100),
        default="system",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


async def init_db():
    """Initializes the database by enabling pgvector extension and creating tables."""
    async with engine.begin() as conn:
        # Ensure pgvector extension is activated in PostgreSQL
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        # Create all tables registered with Base
        await conn.run_sync(Base.metadata.create_all)

async def retrieve_relevant_documents(
    query_embeddings: List[float],
    limit: int = 3,
    distance_threshold: float = 0.6,
) -> List[DocumentRecord]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(DocumentRecord)
            .where(DocumentRecord.embedding.cosine_distance(query_embeddings) <= distance_threshold)
            .order_by(DocumentRecord.embedding.cosine_distance(query_embeddings))
            .limit(limit)
        )
        return list(result.scalars().all())


# if __name__ == "__main__":
#     asyncio.run(init_db())
if __name__ == "__main__":
    async def test_search():
        from document_agent_and_auditor.embedding_factory import get_embeddings_factory

        # 1. Ask a question and embed it
        question = "What is the transformer architecture and attention mechanism?"
        factory = get_embeddings_factory("gemini")
        query_vector = factory.get_embeddings().embed_query(question)

        # 2. Search database using your new function!
        results = await retrieve_relevant_documents(query_vector, limit=1)

        print(f"\nFound {len(results)} matching document(s):")
        for doc in results:
            print("File:", doc.file_path)
            print("Summary Preview:\n", doc.summary[:200], "...")

    asyncio.run(test_search())

    
