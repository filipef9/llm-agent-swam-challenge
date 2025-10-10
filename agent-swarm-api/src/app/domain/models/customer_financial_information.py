from typing import List, Literal

from pydantic import BaseModel, Field


class CustomerFinancialInfoInput(BaseModel):
    """Input schema for the financial information tool."""

    customer_id: str = Field(description="The ID of the customer to query.")

    info_type: Literal["transactions", "receivables"] = Field(
        description="The type of financial information to retrieve"
    )


class Transaction(BaseModel):
    date: str
    amount: float
    status: Literal["Pending", "Approved", "Rejected"]

    def __str__(self):
        return f"Transaction[date={self.date}, amount={self.amount:.2f}, status={self.status}]"


class Transactions(BaseModel):
    name: str
    account_status: Literal["Active", "Inactive"]
    transactions: List[Transaction] = []

    def __str__(self):
        transactions_list = ", ".join(
            str(transaction) for transaction in self.transactions
        )
        return f"Transactions[name={self.name}, account_status={self.account_status}, transactions=[{transactions_list}]]"


class Receivable(BaseModel):
    due_date: str
    amount: float
    status: Literal["Pending", "Approved", "Rejected"]

    def __str__(self):
        return f"Receivable[due_date={self.due_date}, amount={self.amount:.2f}, status={self.status}]"


class Receivables(BaseModel):
    name: str
    account_status: Literal["Active", "Inactive"]
    receivables: List[Receivable] = []

    def __str__(self):
        receivables_list = ", ".join(str(receivable) for receivable in self.receivables)
        return f"Receivables[name={self.name}, account_status={self.account_status}, receivables=[{receivables_list}]]"
