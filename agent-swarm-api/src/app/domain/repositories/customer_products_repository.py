from abc import ABC, abstractmethod

from app.domain.models import Products


class CustomerProductsRepository(ABC):

    @abstractmethod
    def get_products_for(customer_id: str) -> Products:
        pass
