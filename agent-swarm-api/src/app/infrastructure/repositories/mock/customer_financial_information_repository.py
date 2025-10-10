from app.domain.models import Receivables, Transactions
from app.domain.repositories import CustomerFinancialInformationRepository

from .mock_customers_db import MOCK_CUSTOMER_DB


class MockCustomerFinancialInformationRepositoryImpl(
    CustomerFinancialInformationRepository
):

    def get_transactions_for(self, customer_id: str) -> Transactions:
        customer_data = MOCK_CUSTOMER_DB.get(customer_id)

        if not customer_data:
            return None

        return Transactions(
            name=customer_data["name"],
            account_status=customer_data["account_status"],
            transactions=customer_data["transaction_history"],
        )

    def get_receivables_for(self, customer_id: str) -> Receivables:
        customer_data = MOCK_CUSTOMER_DB.get(customer_id)

        if not customer_data:
            return None

        return Receivables(
            name=customer_data["name"],
            account_status=customer_data["account_status"],
            receivables=customer_data["receivables"],
        )
