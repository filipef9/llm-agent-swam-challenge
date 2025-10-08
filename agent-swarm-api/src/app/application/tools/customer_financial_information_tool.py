from typing import Literal

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from app.domain.models import FinancialInfoInput


class GetFinancialInformationTool(BaseTool):
    """Tool to retrieve transaction history of future receivables"""

    def __init__(self, repository: CustomerFinancialInformationRepository):
        self.repository = repository

    name = "get_financial_information"

    description = (
        "Retrieves financial information for a customer. "
        "Use 'transactions' for questions about past sales. "
        "Use 'receivables' for questions about future amounts to be received."
    )

    args_schema: type[BaseModel] = FinancialInfoInput

    def _run(
        self, customer_id: str, info_type: Literal["transactions", "receivables"]
    ) -> str:
        if info_type == "transactions":
            transactions = self.repository.get_transactions_for(customer_id)
            if not transactions:
                return f"The customer with ID '{customer_id}' does not have any transactions."
            return str(transactions)

        if info_type == "receivables":
            receivables = self.repository.get_receivables_for(customer_id)
            if not receivables:
                return f"The customer with ID '{customer_id}' does not have any receivables."
            return str(receivables)
