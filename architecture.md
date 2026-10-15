State:
    file_path
    document_content
    summary
    audit_notes
    status
    iteration_count

langgraph nodes:
    [START]
    ↓
    1. Parser Node (extracts text from file)
    ↓
    2. Summarizer Node (drafts or refines summary)
    ↓
    3. Auditor Node (reviews against source text)
    ↓
    [Conditional Router]
    ├── If Approved                       → 4. Persist to DB → [END]
    ├── If Rejected & iterations < 3      → (Loops back to Summarizer)
    └── If Rejected & iterations >= 3     → 5. HITL (Human Review) → [END]

project start commands:
    uv init
    uv venv