from typing import Optional

from app.domain.models import Products
from app.domain.repositories import CustomerProductsRepository

from .mock_customers_db import MOCK_CUSTOMER_DB


class MockCustomerProductsRepositoryImpl(CustomerProductsRepository):
    def __init__(self):
        pass

    def get_products_for(customer_id: str) -> Optional[Products]:
        customer_data = MOCK_CUSTOMER_DB.get(customer_id)

        if not customer_data:
            return None

        return Products(
            name=customer_data["name"],
            account_status=customer_data["account_status"],
            products=customer_data["products"],
        )
