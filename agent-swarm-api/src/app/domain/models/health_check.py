from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    Model for the health check response.

    Attributes:
        status (str): Current status of the API (e.g., "ok").
        timestamp (str): ISO-formatted timestamp of the health check.
    """

    status: str
    timestamp: str
