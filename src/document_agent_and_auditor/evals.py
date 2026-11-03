import asyncio
from dataclasses import dataclass
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import Faithfulness, ResponseRelevancy, LLMContextPrecisionWithReference
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from document_agent_and_auditor.llm_factory import get_llm_factory
from document_agent_and_auditor.embedding_factory import get_embeddings_factory
from document_agent_and_auditor.rag import answer_document_query


@dataclass(frozen=True)
class BenchmarkSample:
    """Represents a gold-standard evaluation test case."""
    question: str
    reference: str


# Golden benchmark dataset representing diverse evaluation categories
BENCHMARK_SUITE: list[BenchmarkSample] = [
    BenchmarkSample(
        question="Who was the Dalavayi or Chief General of Shivappa Nayaka of Keladi?",
        reference="The Dalavayi or Chief General under Shivappa Nayaka of Keladi was Ediga Timmanna Nayaka.",
    ),
    BenchmarkSample(
        question="By what percentage were operating expenses reduced through cloud migration?",
        reference="Operating expenses were reduced by 5% through cloud migration.",
    ),
    BenchmarkSample(
        question="What is the policy for employee annual performance bonuses and promotions?",
        reference="The available documents do not contain information regarding employee bonuses or promotions.",
    ),
    BenchmarkSample(
        question="What were the primary financial and operational outcomes reported for 2026?",
        reference="Total revenue grew by 15% year-over-year, and operating expenses were reduced by 5% through cloud migration.",
    ),
]


async def run_evaluation_suite() -> None:
    """Executes all benchmark cases through the live RAG pipeline and scores with Ragas."""
    print(f"--- 1. Executing {len(BENCHMARK_SUITE)} queries through live RAG pipeline ---")
    
    questions = [sample.question for sample in BENCHMARK_SUITE]
    references = [sample.reference for sample in BENCHMARK_SUITE]
    
    responses = []
    for q in questions:
        res = await answer_document_query(q)
        responses.append(res)

    eval_dataset = {
        "user_input": questions,
        "response": [r.answer for r in responses],
        "retrieved_contexts": [r.contexts for r in responses],
        "reference": references,
    }
    dataset = Dataset.from_dict(eval_dataset)

    # Initialize Gemini as the LLM & Embedding Judge
    judge_llm = LangchainLLMWrapper(get_llm_factory("low").get_llm())
    judge_embeddings = LangchainEmbeddingsWrapper(get_embeddings_factory("gemini").get_embeddings())

    print("\n--- 2. Running Automated Ragas Evaluation with Gemini Judge ---")
    results = evaluate(
        dataset=dataset,
        metrics=[
            Faithfulness(),
            ResponseRelevancy(strictness=1),
            LLMContextPrecisionWithReference(),
        ],
        llm=judge_llm,
        embeddings=judge_embeddings,
    )

    print("\n=== Evaluation Summary ===")
    print(results)
    
    print("\n=== Detailed Benchmark Scorecard ===")
    df = results.to_pandas()
    cols = [col for col in ["user_input", "faithfulness", "answer_relevancy", "context_precision"] if col in df.columns]
    print(df[cols].to_string(index=False))


if __name__ == "__main__":
    asyncio.run(run_evaluation_suite())