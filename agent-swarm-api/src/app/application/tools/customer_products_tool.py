from langchain_core.tools import BaseTool
from pydantic import BaseModel

from app.domain.models import ProductsStatusInput
from app.domain.repositories import CustomersProductsRepository


class GetCustomerProductsTool(BaseTool):
    """Tool to retrieve a customer's acquired products and account status."""

    def __init__(self, repository: CustomersProductsRepository):
        self.repository = repository

    name = "get_customer_products_and_status"
    description = (
        "Retrieves the acquired products (e.g., card machines) and account status of an InfinitePay customer"
        "Use this for questions about what products the customer has or their general account status."
    )
    args_schema: type[BaseModel] = ProductsStatusInput

    def _run(self, customer_id: str) -> str:
        customer_products = self.repository.get_products_for(customer_id)

        if not customer_products or not customer_products.products:
            return f"The customer with ID '{customer_id}' does not have any products."

        return str(customer_products)
