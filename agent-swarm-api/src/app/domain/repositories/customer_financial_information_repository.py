from abc import ABC, abstractmethod

from app.domain.models import Receivables, Transactions


class CustomerFinancialInformationRepository(ABC):

    @abstractmethod
    def get_transactions_for(self, customer_id: str) -> Transactions:
        pass

    @abstractmethod
    def get_receivables_for(self, customer_id: str) -> Receivables:
        pass
