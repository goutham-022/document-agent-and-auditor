from typing import Literal
from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from document_agent_and_auditor.utils.config import GEMINI_LLM_API_KEY


class BaseLLMFactory(ABC):
    @abstractmethod
    def get_llm(self) -> BaseChatModel:
        pass

class GeminiLLMFactory(BaseLLMFactory):
    def __init__(self):
        pass

    def get_llm(self) -> BaseChatModel:
        return ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            # model="gemini-3.6-flash",
            temperature=0.0,
            api_key=GEMINI_LLM_API_KEY,
        )

def get_llm_factory(tier: Literal["low", "medium", "high"]) -> BaseLLMFactory:
    if tier in ["low", "medium", "high"]:
        return GeminiLLMFactory()
    else:
        raise ValueError(f"Unsupported tier: {tier}")

if __name__ == "__main__":
    llm_factory = get_llm_factory("low")
    llm = llm_factory.get_llm()
    response = llm.invoke("Hello, how are you?")
    print(response.content)