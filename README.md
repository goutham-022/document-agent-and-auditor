# The Enterprise Document Agent & Auditor

An agentic backend system built with **LangGraph**, **Google Gemini**, **FastAPI**, and **PostgreSQL (pgvector)**.

The system processes enterprise documents through an **Evaluator-Optimizer reflection loop**:
1. **Parser Node:** Ingests documents (PDF, TXT, MD) and extracts clean text.
2. **Summarizer Node (Agent):** Drafts a structured summary and extracts key highlights.
3. **Auditor Node (Critic):** Cross-checks the draft against the source text to detect hallucinations, discrepancies, or missing critical points.
4. **Reflection Loop:** If discrepancies are found, the Auditor provides actionable feedback to the Summarizer (up to a max retry limit before escalating to human review).
5. **Storage & Search:** Stores approved documents and vector embeddings in PostgreSQL with `pgvector` for future semantic search and audit trails.

## Tech Stack
- **Orchestration:** LangGraph
- **LLM:** Google Gemini (`langchain-google-genai`)
- **API Framework:** FastAPI + Uvicorn
- **Database:** PostgreSQL + pgvector + SQLAlchemy (asyncpg)
- **Package Manager:** `uv`

## Getting Started

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/goutham-022/document-agent-and-auditor.git
cd document-agent-and-auditor

# Create and activate virtual environment
uv venv
.\.venv\Scripts\activate

# Install dependencies
uv add -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your_gemini_api_key_here"
```
