from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ProductsStatusInput(BaseModel):
    """Input schema for the customer products tool."""

    customer_id: str = Field(description="The ID of the customer to query.")


class Product(BaseModel):
    product_name: str
    serial_number: Optional[str]
    status: Literal["Active", "Inactive"]

    def __str__(self):
        return f"Product[product_name={self.product_name}, serial_number={self.serial_number or 'N/A'}, status={self.status}]"


class Products(BaseModel):
    name: str
    account_status: Literal["Active", "Inactive"]
    products: List[Product] = []

    def __str__(self):
        products_list = ", ".join(str(product) for product in self.products)
        return f"Products[name={self.name}, account_status={self.account_status}, products=[{products_list}]]"
