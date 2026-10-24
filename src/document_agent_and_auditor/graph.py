import asyncio
from langgraph.graph import StateGraph, START, END
from document_agent_and_auditor.models import DocumentState
from document_agent_and_auditor.nodes import parser, summarizer, auditor, human_reviewer, embedding_generator, db_writer


workflow = StateGraph(DocumentState)

workflow.add_node("parser", parser)
workflow.add_node("summarizer", summarizer)
workflow.add_node("auditor", auditor)
workflow.add_node("human_reviewer", human_reviewer)
workflow.add_node("embedding_generator", embedding_generator)
workflow.add_node("db_writer", db_writer)


def route_after_audit(state: DocumentState) -> str:
    if state.status == "rejected":
        if state.iteration_count < state.maximum_iteration:
            return "summarizer"
        else:
            return "human_reviewer"
    elif state.status == "approved":
        return "embedding_generator"
    else:
        raise ValueError(f"Unknown document status encountered: {state.status}")

def route_after_human_review(state: DocumentState) -> str:
    if state.status == "rejected":
        return "summarizer"
    elif state.status == "approved":
        return "embedding_generator"
    else:
        raise ValueError(f"Unknown document status encountered: {state.status}")

workflow.add_edge(START, "parser")
workflow.add_edge("parser", "summarizer")
workflow.add_edge("summarizer", "auditor")
workflow.add_conditional_edges("auditor", route_after_audit, [
    "summarizer",
    "human_reviewer",
    "embedding_generator"
])

workflow.add_conditional_edges("human_reviewer", route_after_human_review, [
    "summarizer",
    "embedding_generator"
])
workflow.add_edge("embedding_generator", "db_writer")
# TODO: Connect actual PostgreSQL + pgvector persistence in Week 2 once DB is configured
workflow.add_edge("db_writer", END)

app = workflow.compile()

if __name__ == "__main__":
    # png_bytes = app.get_graph().draw_mermaid_png()
    # with open("graph.png", "wb") as f:
    #     f.write(png_bytes)
    # print("Graph saved as graph.png!")
    async def main():
        initial_state = DocumentState(file_path="sample_testing.txt")
        final_state = await app.ainvoke(initial_state)

        print("\n" + "=" * 45)
        print("       WORKFLOW EXECUTION COMPLETE")
        print("=" * 45)
        print(f"File Path:        {final_state.get('file_path')}")
        print(f"Final Status:     {final_state.get('status')}")
        print(f"Total Iterations: {final_state.get('iteration_count')}")
        print(f"Auditor Feedback: {final_state.get('feedback')}")
        summary = final_state.get('summary') or ""
        print(f"Summary Length:   {len(summary)} characters")
        embeddings = final_state.get('embeddings') or []
        print(f"Vector Dimension: {len(embeddings)} floats")
        print("Output Saved:     summary_output.md & PostgreSQL DB")
        print("=" * 45)

    asyncio.run(main())