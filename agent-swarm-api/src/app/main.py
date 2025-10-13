from fastapi import FastAPI

from app.routers import chat_v1_router, docs_router, health_router
from app.utils import config

app = FastAPI(
    title=config["APITitle"],
    version=config["APIVersion"],
    description=config["APIDescription"],
    root_path=config["APIRootPath"],
)

app.include_router(docs_router)
app.include_router(health_router)
app.include_router(chat_v1_router)
