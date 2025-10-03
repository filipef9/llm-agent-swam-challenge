from typing import Literal, Optional

from pydantic import BaseModel


class RouterAgentState(BaseModel):
    user_id: str
    message: str
    next_agent: Optional[Literal["knowledge_agent", "customer_support_agent"]] = None
    answer: Optional[str] = None


class Router(BaseModel):
    """Agent to route to next."""

    next: Literal["knowledge_agent", "customer_support_agent"]
