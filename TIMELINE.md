# Project Tracker & Timeline: The Enterprise Document Agent & Auditor

> **Working Schedule:** 1 hour/day × 7 days/week (Daily, No Rest Days!)  
> **Target:** 7 hrs/week | **Kickoff:** October 13, 2026 (Day 1)  
> - `✅ Completed` — Fully finished and verified with Git commit.  
> - `⚠️ Partially Achieved / Missed` — Incomplete or missed session.  
> - `⏳ In Progress` — Active task currently being worked on.  
> - `⏹️ Pending` — Scheduled for future session.

---

## 📅 Week 1: Foundations & Core Node Creation (Days 1 – 7: Oct 13 – Oct 19)
**Goal:** Inception, environment setup, and implementing all 5 agent nodes.

| Day | Date | Milestone & Deliverables | Status | Notes / Artifacts |
| :---: | :---: | :--- | :---: | :--- |
| **Day 1** | **Oct 13** | **Project Inception & Architecture Planning**<br>• Defined problem statement & tech stack (LangGraph, Gemini, pgvector) | ✅ Completed | Architecture aligned. |
| **Day 2** | **Oct 14** | **System Design & State Schemas**<br>• Planned Evaluator-Optimizer loop and state attributes | ✅ Completed | Flow approved. |
| **Day 3** | **Oct 15** | **Repository Setup & Foundations**<br>• Repo init with `uv`, `.venv`, `.gitignore`<br>• Created `architecture.md` and `README.md` | `a45acbe` ✅ | Synced with remote GitHub. |
| **Day 4** | **Oct 16** | **LLM Factory & First Nodes**<br>• `config.py` `.env` reader<br>• `LLMFactory` (Gemini 3.5 Flash-Lite abstract factory)<br>• `parser` (PDF, TXT, MD) & `summarizer` nodes | `af933cf` ✅ | Verified on `sample_testing.txt`. |
| **Day 5** | **Oct 17** | **Auditor Node & Structured Schema**<br>• Created `models.py` (`DocumentState`, `AuditResponse`)<br>• `auditor` node with structured output evaluation | `d56f5ae` ✅ | Saved output to `summary_output.md`. |
| **Day 6** | **Oct 18** | **Human Reviewer & DB Writer Nodes**<br>• Implemented `human_reviewer` node with admin escalation prompt<br>• Stubbed `db_writer` node with placeholder<br>• Updated `summarizer` to auto-write `summary_output.md` | ✅ Completed | All 5 nodes defined & verified. |
| **Day 7** | **Oct 19** | **Missed Session**<br>• No work done | ⚠️ Missed | 0h logged. |

---

## 📅 Week 2: Graph Assembly & PostgreSQL / pgvector (Days 8 – 14: Oct 20 – Oct 26)
**Goal:** Assemble the LangGraph workflow, implement conditional reflection routing, and set up pgvector.

| Day | Date | Task / Milestone | Status | Notes / Reason |
| :---: | :---: | :--- | :---: | :--- |
| **Day 8** | **Oct 20** | **Graph Assembly (`graph.py`)**<br>• Design & initialize `StateGraph(DocumentState)`<br>• Register all 5 nodes<br>• Add entrypoint and linear flow edges | ✅ Completed | Fully assembled, conditional routers (`route_after_audit`, `route_after_human_review`) implemented, compiled, and visual graph verified. |
| **Day 9** | **Oct 21** | **Conditional Router (`should_continue`)**<br>• Implement conditional edge logic from `auditor`<br>• Loop: `rejected` & count < 3 $\rightarrow$ `summarizer`<br>• Escalation: `rejected` & count $\ge$ 3 $\rightarrow$ `human_reviewer`<br>• Success: `approved` $\rightarrow$ `db_writer` | ✅ Completed | Implemented `route_after_audit` (with reflection & escalation bounds) and `route_after_human_review`. Completed: Oct 20, 2026. |
| **Day 10** | **Oct 22** | **End-to-End Agent Verification**<br>• Test happy path (instant approval)<br>• Test reflection loop (revision via feedback)<br>• Test max-iteration escalation path | ✅ Completed | Verified all 3 execution paths (Happy Path, Reflection Loop, and Human Escalation). Completed: Oct 20, 2026. |
| **Day 11** | **Oct 23** | **Formal Test Refactoring (Deferred to Week 4)**<br>• Unit/integration tests with `pytest` moved to Week 4 alongside CI/CD<br>• Merge `feature-1` $\rightarrow$ `main` scheduled after `db_writer` persistence verification | ⏹️ Pending | Deferred to align with CI/CD and finalize features first. |
| **Day 12** | **Oct 24** | **PostgreSQL + pgvector Setup (`db.py`)**<br>• Start PostgreSQL with `pgvector` in Docker (port 5433)<br>• Configure async connection via SQLAlchemy / `asyncpg` | ✅ Completed | Docker container verified, `.env` configured, async engine and connection pool verified. Completed: Oct 21, 2026. |
| **Day 13** | **Oct 25** | **Database Schema & Embedding Factory**<br>• Define table schema (UUID, metadata, text, summary, `Vector(768)`)<br>• Execute `init_db()` DDL migration<br>• Add Gemini text embeddings (`gemini-embedding-001`, 768-dim) in `embedding_factory.py` | ✅ Completed | Schema & table created in Docker Postgres. Embedding factory built & verified live with Google Gemini. Completed: Oct 22, 2026. |
| **Day 14** | **Oct 26** | **Wire `db_writer` & `embedding_generator` Nodes to PostgreSQL**<br>• Added explicit `embedding_generator` node to graph<br>• Implemented async `db_writer` to persist document, summary, and vectors to database | ✅ Completed | Executed full async pipeline end-to-end (`app.ainvoke`). Verified row and 768-dim vector in PostgreSQL via pgAdmin. Completed: Oct 24, 2026. |




---

## 📅 Week 3: RAG Pipeline, Guardrails & Evals (Days 15 – 21: Oct 27 – Nov 02)
**Goal:** Vector similarity search, RAG Q&A, guardrails, and hallucination evaluation.

| Day | Date | Task / Milestone | Status | Notes / Reason |
| :---: | :---: | :--- | :---: | :--- |
| **Day 15** | **Oct 27** | **Vector Similarity Search Query**<br>• Write cosine similarity search (`<=>` operator) in `db.py`<br>• Test top-$k$ retrieval | ⏹️ Pending | |
| **Day 16** | **Oct 28** | **RAG Question-Answering Chain**<br>• Query $\rightarrow$ Embedding $\rightarrow$ Search $\rightarrow$ Synthesize response with citations | ⏹️ Pending | |
| **Day 17** | **Oct 29** | **FastAPI Integration (`api.py`)**<br>• `POST /upload` (runs agent)<br>• `POST /query` (runs RAG)<br>• Test with Swagger UI | ⏹️ Pending | |
| **Day 18** | **Oct 30** | **Input Guardrails & PII Protection**<br>• PII detection/masking<br>• Prompt injection protection before parser | ⏹️ Pending | |
| **Day 19** | **Oct 31** | **Evals Setup (Ragas / DeepEval)**<br>• Setup evaluation library<br>• Create benchmark dataset of documents | ⏹️ Pending | |
| **Day 20** | **Nov 01** | **Benchmark Suite & Auditor Calibration**<br>• Measure Faithfulness & Answer Relevance<br>• Tune auditor thresholds | ⏹️ Pending | |
| **Day 21** | **Nov 02** | **Git Milestone & Review**<br>• Merge `feature-2-db` $\rightarrow$ `main`<br>• Create `feature-3-docker-k8s` | ⏹️ Pending | |

---

## 📅 Week 4: Docker, Kubernetes & AWS Cloud (Days 22 – 28: Nov 03 – Nov 09)
**Goal:** Containerization, K8s orchestration, CI/CD, and AWS deployment.

| Day | Date | Task / Milestone | Status | Notes / Reason |
| :---: | :---: | :--- | :---: | :--- |
| **Day 22** | **Nov 03** | **Multi-Stage Production `Dockerfile`**<br>• Optimized build leveraging `uv`<br>• Verify image boots cleanly | ⏹️ Pending | |
| **Day 23** | **Nov 04** | **Local Multi-Container (`docker-compose.yml`)**<br>• Compose file with FastAPI + `pgvector/pgvector:pg16`<br>• 1-click startup | ⏹️ Pending | |
| **Day 24** | **Nov 05** | **Core Kubernetes Manifests (`k8s/`)**<br>• `deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml` | ⏹️ Pending | |
| **Day 25** | **Nov 06** | **K8s Ingress, Auto-scaling (`hpa.yaml`) & Local Testing**<br>• Test on Minikube / Kind<br>• Verify rolling updates & pod health | ⏹️ Pending | |
| **Day 26** | **Nov 07** | **CI/CD Pipeline (GitHub Actions)**<br>• `.github/workflows/ci.yml` (lint, pytest, push to ECR) | ⏹️ Pending | |
| **Day 27** | **Nov 08** | **AWS Cloud Infrastructure & Deployment**<br>• AWS ECR, RDS PostgreSQL with pgvector, ECS/EKS deployment<br>• Live cloud testing | ⏹️ Pending | |
| **Day 28** | **Nov 09** | **Project Wrap-up & Portfolio Release**<br>• Observability (LangSmith/Langfuse)<br>• Final documentation, architecture diagram, demo video | ⏹️ Pending | |
