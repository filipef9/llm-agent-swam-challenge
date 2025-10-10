from langchain_core.tools import BaseTool
from pydantic import BaseModel, ConfigDict

from app.domain.models import ProductsStatusInput
from app.domain.repositories import CustomerProductsRepository


class GetCustomerProductsTool(BaseTool):
    """Tool to retrieve a customer's acquired products and account status."""

    name: str = "get_customer_products_and_status"

    description: str = (
        "Retrieves the acquired products (e.g., card machines) and account status of an InfinitePay customer. "
        "Use this for questions about what products the customer has or their general account status."
    )

    args_schema: type[BaseModel] = ProductsStatusInput

    model_config = ConfigDict(extra="allow")

    def __init__(self, repository: CustomerProductsRepository):
        super().__init__()
        self.repository = repository

    def _run(self, customer_id: str) -> str:
        customer_products = self.repository.get_products_for(customer_id)

        if not customer_products or not customer_products.products:
            return f"The customer with ID '{customer_id}' does not have any products."

        return str(customer_products)
