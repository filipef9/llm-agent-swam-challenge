MOCK_CUSTOMER_DB = {
    "client789": {
        "customer_id": "client789",
        "name": "Golden Bean Coffee Shop",
        "email": "contact@goldenbean.com",
        "account_status": "Active",
        "active_since": "2023-01-20",
        "products": [
            {
                "product_name": "InfiniteSmart",
                "serial_number": "IS-123456",
                "status": "Active",
            },
            {"product_name": "InfiniteTap", "status": "Active"},
        ],
        "transaction_history": [
            {"date": "2025-10-06", "amount": 45.50, "status": "Approved"},
            {"date": "2025-10-05", "amount": 120.00, "status": "Approved"},
        ],
        "receivables": [
            {"due_date": "2025-10-08", "amount": 350.00, "status": "Pending"},
            {"due_date": "2025-10-09", "amount": 150.75, "status": "Pending"},
        ],
    }
}
