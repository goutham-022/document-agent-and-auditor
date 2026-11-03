# Project Timesheet: The Enterprise Document Agent & Auditor

> **Target Schedule:** 1 hour/day × 7 days/week (Daily, No Rest Days!)  
> **Weekly Goal:** 7 hours/week — consistent daily execution with Git commits.  
> **Project Kickoff:** October 13, 2026 (Day 1)

---

## ⏱️ Daily Log

| Day | Date | Time Window | Duration | Milestone / Focus Area | Commit / Status |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **Day 1** | **2026-10-13** | ~07:00 - 08:00 | ~1h 00m | • Project inception & problem statement definition<br>• Tech stack exploration (LangGraph + Gemini + pgvector) | ✅ Completed |
| **Day 2** | **2026-10-14** | ~07:00 - 08:00 | ~1h 00m | • Evaluator-Optimizer reflection architecture design<br>• State schema planning and repo structuring | ✅ Completed |
| **Day 3** | **2026-10-15** | ~05:00 - 06:00 | ~1h 00m | • Initialized repo with `uv`, `.venv`, `.gitignore`<br>• Created architecture blueprint (`architecture.md`)<br>• Initial project documentation (`README.md`) | `a45acbe` ✅ Completed |
| **Day 4** | **2026-10-16** | ~07:00 - 08:15 | ~1h 15m | • Implemented `config.py` `.env` reader<br>• Built `LLMFactory` (Gemini 3.5 Flash-Lite abstract factory)<br>• Built `parser` (PDF, TXT, MD) & `summarizer` nodes<br>• Tested summary generation on `sample_testing.txt` | `af933cf` ✅ Completed |
| **Day 5** | **2026-10-17** | ~07:30 - 08:45 | ~1h 15m | • Created `models.py` (`DocumentState`, `AuditResponse`)<br>• Built `auditor` node with structured output evaluation<br>• Formatted and saved output to `summary_output.md`<br>• Created master timeline | `d56f5ae` ✅ Completed |
| **Day 6** | **2026-10-18** | 06:20 - 07:15 | ~0h 55m | • Implemented `human_reviewer` node with admin escalation prompt<br>• Stubbed `db_writer` node<br>• Updated `summarizer` to auto-write clean text to `summary_output.md` | ✅ Completed |
| **Day 7** | **2026-10-19** | — | 0h 00m | Missed session / Could not work | ⚠️ Missed session (0h) |
| **Day 8** | **2026-10-20** | 06:56-08:15, 17:57-19:10, 21:39-22:08 | ~3h 05m | • Built and assembled `graph.py` (StateGraph, 5 nodes, linear & conditional edges)<br>• Implemented `route_after_audit` & `route_after_human_review`<br>• Verified all 3 execution paths (Happy Path, Reflection Loop, Human Escalation)<br>• Generated `graph.png` and updated `architecture.md`<br>• Spun up `pgvector` Docker container, connected in pgAdmin & IDE, configured `.env`<br>• Began database connection architecture discussion (`db.py`) | ✅ Completed |
| **Day 9** | **2026-10-21** | 05:21 - 08:15 | ~2h 55m | • Deep conceptual architecture dive: Vector DB vs RDBMS vs NoSQL, RAG vs Text-to-SQL, query generation vs vector distance<br>• Solved large-file storage dilemma (Object Storage URI pointer vs text bloat)<br>• Designed lean `DocumentRecord` schema (UUID PK, `file_path`, `summary`, `created_by`, `Vector(768)`, timestamps)<br>• Installed `greenlet` / updated `requirements.txt`<br>• Executed `init_db()` in `db.py` to enable `vector` extension and successfully create `documents` table in Docker Postgres | ✅ Completed |
| **Day 10** | **2026-10-22** | 05:01 - 05:54 | ~0h 55m | • Built `embedding_factory.py` with `EmbeddingsFactory` & `GeminiEmbeddings` using `gemini-embedding-001` (768 dimensions)<br>• Verified live vector generation with Google Gemini API<br>• Architected explicit `embedding_generator` node (Single Responsibility Principle) & updated `DocumentState`<br>• Updated conditional routing in `graph.py` and rendered fresh `graph.png`<br>• Implemented standard asynchronous `async def db_writer` node in `nodes.py` using `AsyncSessionLocal` and `DocumentRecord` | ✅ Completed |
| **Day 11** | **2026-10-23** | 08:43-09:07, 14:33-14:40 | ~0h 35m | • Deep dive on Pydantic DTOs vs SQLAlchemy ORM Entities<br>• Explored Engine (connection pool) vs AsyncSessionLocal (transaction manager)<br>• Created educational `orm_vs_raw_sql_reference.py` comparing raw asyncpg vs SQLAlchemy ORM<br>• Clarified `CREATE EXTENSION vector` (Postgres server-side) vs `register_vector` (client-side) | ✅ Completed |
| **Day 12** | **2026-10-24** | 05:44 - 06:35 | ~0h 50m | • Clarified `__tablename__`, `DeclarativeBase`, and `__abstract__ = True` base models<br>• Explored `Mapped[...]` type inference and persistent checkpointers vs RAM in LangGraph<br>• Updated `graph.py` to use asynchronous invocation (`await app.ainvoke`)<br>• Booted Docker `doc-agent-db` container<br>• Executed full end-to-end pipeline (Parser $\rightarrow$ Summarizer $\rightarrow$ Auditor $\rightarrow$ Embedder $\rightarrow$ DB Writer)<br>• Verified persisted document and 768-dim vector in PostgreSQL using pgAdmin Query Tool | ✅ Completed |
| **Day 13** | **2026-10-25** | 05:58 - 07:08 | ~1h 10m | • Verified vector search with cosine distance filter (`search_similar_documents` in `db.py`)<br>• Deep dive on raw SQL `<=>` operator vs boolean conditions, and empirical threshold calibration (0.6)<br>• Added grounded `RAG_QA_PROMPT` in `prompts.py`<br>• Began architecting RAG service layer (`answer_document_query` in `rag.py`) | ✅ Completed |
| **Day 14** | **2026-10-26** | — | 0h 00m | Missed session / Could not work | ⚠️ Missed session (0h) |
| **Day 15** | **2026-10-27** | 08:45 - 09:30 | ~0h 45m | • Completed RAG service layer (`answer_document_query` in `rag.py`)<br>• Renamed DB function to `retrieve_relevant_documents`<br>• Context augmentation with source citations and low-temperature Gemini synthesis<br>• Verified end-to-end RAG with relevant query and short-circuit zero-result query | ✅ Completed |
| **Day 16** | **2026-10-28** | 05:11-05:58, 17:24-19:02 | ~2h 25m | • Built modular FastAPI architecture (`main.py` lifespan, `routes.py` APIRouter)<br>• Created Pydantic DTOs (`QueryRequest`, `QueryResponse`, `IngestionResponse`)<br>• Resolved Gemini multimodal block parsing bug in `rag.py`<br>• Live-verified `POST /documents/query` via Swagger UI (positive & negative cases)<br>• Built `service.py` clean service layer with UUID prefixing<br>• Architectural refactor: separated `audit_status` (evaluator verdict) from `doc_upload_status` (DB persistence proof in `db_writer`) across `models.py`, `nodes.py`, `graph.py`, and `service.py`<br>• Completed `POST /documents/upload` endpoint | ✅ Completed |
| **Day 17** | **2026-10-29** | 07:04 - 08:00 | ~0h 55m | • Deep dive on pipeline fault tolerance, failure propagation, and lifecycle states<br>• Enhanced `DocumentState.doc_upload_status: Literal["pending", "success", "failed"] = "pending"`<br>• Implemented `abort` exit in `human_reviewer` node and routed directly to `END` in `graph.py`<br>• Wrapped `db_writer` in try-except to catch DB crashes and set `doc_upload_status = "failed"`<br>• Identified critical audit feedback vs system error leak bug; designed explicit error reporting | ✅ Completed |
| **Day 18** | **2026-10-30** | 16:24 - 18:10 | ~1h 45m | • Added `error_message` to `DocumentState` and isolated error propagation<br>• Implemented file extension perimeter guardrail in `service.py`<br>• Verified end-to-end `/upload` ingestion and RAG querying in Swagger UI<br>• Built prompt injection detection engine in `guardrails.py` | 🔄 In Progress |
| **Day 19** | **2026-10-31** | — | 0h 00m | Missed session / Could not work | ⚠️ Missed session (0h) |
| **Day 20** | **2026-11-01** | 08:55 - 09:25 | ~0h 30m | • Integrated `detect_prompt_injection` guardrail in `nodes.py` (`parser` node)<br>• Added conditional edge `check_guardrail` in `graph.py` routing malicious files to `END`<br>• Wired prompt injection guardrail in `rag.py` (`_check_guardrails`) before DB retrieval | ✅ Completed |
| **Day 21** | **2026-11-02** | — | 0h 00m | Missed session / Could not work | ⚠️ Missed session (0h) |
| **Day 22** | **2026-11-03** | 09:23 - 10:25, 11:10 - 12:05, 16:20 - 17:25 | ~3h 00m | • Completed `mask_pii` (emails, phone, credit card, SSN, Aadhaar) in `guardrails.py`<br>• Wired PII redaction into `nodes.py` (parser) and `rag.py` (query)<br>• Live-verified prompt injection blocking and PII masking via Swagger UI<br>• Guardrails vs Evals conceptual deep dive and Ragas Triad breakdown<br>• Solved Windows asyncpg closed event loop issue in `evals.py`<br>• Built automated Ragas evaluation suite in `evals.py` with Gemini Judge<br>• Achieved 100% Faithfulness, 82.3% Relevancy, 87.5% Context Precision across 4 benchmark cases | ✅ Completed |

---

## 📊 Summary by Week

| Week | Days | Date Range | Target Hours | Logged Hours | Status |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Week 1** | Days 1 – 7 | Oct 13 – Oct 19 | 7h 00m | ~6h 25m | ✅ Finished |
| **Week 2** | Days 8 – 14 | Oct 20 – Oct 26 | 7h 00m | ~9h 30m | 🌟 Exceeded Target |
| **Week 3** | Days 15 – 21 | Oct 27 – Nov 02 | 7h 00m | ~6h 10m | ✅ Finished |
| **Week 4** | Days 22 – 28 | Nov 03 – Nov 09 | 7h 00m | ~3h 00m *(Active)* | 🔄 In Progress |
| **Week 5** | Days 29 – 35 | Nov 10 – Nov 16 | 7h 00m | 0h 00m | ⏹️ Planned (Deep Dive & Interview Prep) |


