from fastapi import Depends
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools import BaseTool
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_tavily import TavilySearch

from app.application.agents import CustomerSupportAgent, KnowledgeAgent, RouterAgent
from app.application.tools import (
    GetCustomerFinancialInformationTool,
    GetCustomerProductsTool,
)
from app.application.usecases import ChatUseCase
from app.domain.repositories import (
    CustomerFinancialInformationRepository,
    CustomerProductsRepository,
)
from app.infrastructure.repositories import (
    MockCustomerFinancialInformationRepositoryImpl,
    MockCustomerProductsRepositoryImpl,
)
from app.utils import config


def get_llm() -> BaseChatModel:
    return ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.0)


def get_vector_store_retriever(llm: BaseChatModel = Depends(get_llm)) -> BaseRetriever:
    embedding = HuggingFaceEmbeddings(model_name=config["EmbeddingModel"])
    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embedding,
        collection_name=config["VectorStoreCollectionName"],
        url=config["VectorStoreURL"],
    )
    return MultiQueryRetriever.from_llm(retriever=vector_store.as_retriever(), llm=llm)


def get_web_search_tool() -> BaseTool:
    return TavilySearch(max_results=5)


def get_knowledge_agent(
    llm: BaseChatModel = Depends(get_llm),
    vector_store_retriever: BaseRetriever = Depends(get_vector_store_retriever),
    web_search_tool: BaseTool = Depends(get_web_search_tool),
) -> KnowledgeAgent:
    return KnowledgeAgent(
        llm=llm,
        vector_store_retriever=vector_store_retriever,
        web_search_tool=web_search_tool,
    )


def get_customer_products_repository() -> CustomerProductsRepository:
    return MockCustomerProductsRepositoryImpl()


def get_customer_products_tool(
    repository: CustomerProductsRepository = Depends(get_customer_products_repository),
) -> BaseTool:
    return GetCustomerProductsTool(repository=repository)


def get_customer_financial_information_repository() -> (
    CustomerFinancialInformationRepository
):
    return MockCustomerFinancialInformationRepositoryImpl()


def get_customer_financial_information_tool(
    repository: CustomerFinancialInformationRepository = Depends(
        get_customer_financial_information_repository
    ),
) -> BaseTool:
    return GetCustomerFinancialInformationTool(repository=repository)


def get_customer_support_agent(
    llm: BaseChatModel = Depends(get_llm),
    customer_products_tool: BaseTool = Depends(get_customer_products_tool),
    customer_financial_information_tool: BaseTool = Depends(
        get_customer_financial_information_tool
    ),
) -> CustomerSupportAgent:
    return CustomerSupportAgent(
        llm=llm,
        customer_products_tool=customer_products_tool,
        customer_financial_information_tool=customer_financial_information_tool,
    )


def get_router_agent(
    llm: BaseChatModel = Depends(get_llm),
    knowledge_agent: KnowledgeAgent = Depends(get_knowledge_agent),
    customer_support_agent: CustomerSupportAgent = Depends(get_customer_support_agent),
) -> RouterAgent:
    return RouterAgent(
        llm=llm,
        knowledge_agent=knowledge_agent,
        customer_support_agent=customer_support_agent,
    )


def get_chat_usecase(
    router_agent: RouterAgent = Depends(get_router_agent),
) -> ChatUseCase:
    return ChatUseCase(router_agent=router_agent)
