from typing import Literal, Optional

from pydantic import BaseModel


class KnowledgeAgentState(BaseModel):
    user_id: str
    message: str
    knowledgebase: Optional[str] = None
    selected_retriever: Optional[Literal["vector_store", "web_search"]] = None
    answer: Optional[str] = None


class RouterRetriever(BaseModel):
    """Select retriever to use."""

    selected_retriever: Literal["vector_store", "web_search"]
