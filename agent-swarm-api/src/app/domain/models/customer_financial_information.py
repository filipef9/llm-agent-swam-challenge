from typing import Literal

from pydantic import BaseModel, Field


class FinancialInfoInput(BaseModel):
    """Input schema for the financial information tool."""

    customer_id: str = Field(description="The ID of the customer to query.")

    info_type: Literal["transactions", "receivables"] = Field(
        description="The type of financial information to retrieve"
    )
