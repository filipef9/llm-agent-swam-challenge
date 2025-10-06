from fastapi import Depends
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel

from app.application.agents import CustomerSupportAgent, KnowledgeAgent, RouterAgent
from app.application.usecases import ChatUseCase


def get_llm() -> BaseChatModel:
    return ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.0)


def get_knowledge_agent(llm: BaseChatModel = Depends(get_llm)) -> KnowledgeAgent:
    return KnowledgeAgent(llm=llm)


def get_customer_support_agent() -> CustomerSupportAgent:
    return CustomerSupportAgent()


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
