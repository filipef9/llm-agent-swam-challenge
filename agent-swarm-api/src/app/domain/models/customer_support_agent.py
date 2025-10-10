from typing import Annotated, Optional

from langgraph.graph.message import add_messages
from pydantic import BaseModel


class CustomerSupportAgentState(BaseModel):
    user_id: str
    message: str
    messages: Annotated[list, add_messages]
    answer: Optional[str] = None
