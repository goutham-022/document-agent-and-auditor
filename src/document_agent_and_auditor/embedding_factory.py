from abc import ABC, abstractmethod
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from document_agent_and_auditor.utils.config import GEMINI_LLM_API_KEY

class EmbeddingsFactory(ABC):
    @abstractmethod
    def get_embeddings(self):
        pass

class GeminiEmbeddings(EmbeddingsFactory):
    def __init__(self):
        pass

    def get_embeddings(self):
        return GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            output_dimensionality=768,
            google_api_key=GEMINI_LLM_API_KEY,
        )

def get_embeddings_factory(model_name: str) -> EmbeddingsFactory:
    if model_name == "gemini":
        return GeminiEmbeddings()
    else:
        raise ValueError("Invalid model name")

if __name__ == "__main__":
    factory = get_embeddings_factory("gemini")
    embeddings = factory.get_embeddings()
    vector = embeddings.embed_query("This is a test document summary.")
    print(f"Success! Vector length: {len(vector)}")
    print(f"Sample values: {vector[:5]}...")