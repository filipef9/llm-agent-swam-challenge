from typing import Literal

from langchain_core.tools import BaseTool
from pydantic import BaseModel, ConfigDict

from app.domain.models import CustomerFinancialInfoInput
from app.domain.repositories import CustomerFinancialInformationRepository


class GetCustomerFinancialInformationTool(BaseTool):
    """Tool to retrieve transaction history of future receivables"""

    name: str = "get_financial_information"

    description: str = (
        "Retrieves financial information for a customer. "
        "Use 'transactions' for questions about past sales. "
        "Use 'receivables' for questions about future amounts to be received."
    )

    args_schema: type[BaseModel] = CustomerFinancialInfoInput

    model_config = ConfigDict(extra="allow")

    def __init__(self, repository: CustomerFinancialInformationRepository):
        super().__init__()
        self.repository = repository

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
