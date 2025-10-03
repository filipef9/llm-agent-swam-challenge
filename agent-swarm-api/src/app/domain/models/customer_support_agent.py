from typing import Optional

from pydantic import BaseModel


class CustomerSupportAgentState(BaseModel):
    user_id: str
    message: str
    answer: Optional[str] = None
