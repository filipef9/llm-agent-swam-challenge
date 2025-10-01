import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import docs_router, health_router
from app.utils import config

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("API has started up")
        yield
    finally:
        logger.info("API has shutdown")


app = FastAPI(
    title=config["APITitle"],
    version=config["APIVersion"],
    description=config["APIDescription"],
    root_path=config["APIRootPath"],
    lifespan=lifespan,
)

app.include_router(docs_router)
app.include_router(health_router)
# app.include_router(swarm_v1.router)
