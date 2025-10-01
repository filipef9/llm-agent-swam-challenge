from fastapi import Depends

from app.application.agents import RouterAgent
from app.application.usecases import ChatUseCase


def get_router_agent() -> RouterAgent:
    return RouterAgent


def get_chat_usecase(
    router_agent: RouterAgent = Depends(get_router_agent),
) -> ChatUseCase:
    return ChatUseCase(router_agent=router_agent)
