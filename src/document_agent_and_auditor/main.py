import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from document_agent_and_auditor.routes import router as document_router
from document_agent_and_auditor.db import init_db

load_dotenv()

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("starting!....")
    await init_db()
    yield
    print("ending!....")

app = FastAPI(
    title="Enterprise Document Agent & Auditor API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(document_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("document_agent_and_auditor.main:app", host="0.0.0.0", port=8000, reload=True)