import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.usecases import ChatUseCase
from app.dependencies import get_chat_usecase
from app.domain.models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

chat_v1_router = APIRouter(prefix="/v1")


@chat_v1_router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, usecase: ChatUseCase = Depends(get_chat_usecase)
) -> ChatResponse:
    try:
        response = usecase.execute(user_id=request.user_id, message=request.message)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error("Error processing request: %s", e, exc_info=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error while processing the request",
        )
