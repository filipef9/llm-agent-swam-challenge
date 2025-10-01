import logging

from fastapi import APIRouter, HTTPException, status

from app.domain.models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

chat_v1_router = APIRouter(prefix="/v1")


@chat_v1_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        return ChatResponse(response="Hello, world!")
    except Exception as e:
        logger.error("Error processing request: %s", e, exc_info=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error while processing the request",
        )
