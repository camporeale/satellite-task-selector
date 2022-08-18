"""Main module"""
import sys
from loguru import logger
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.buffer import task_buffer
from app.config import get_settings
from app.routers import tasks_router

app = FastAPI(title="Satellite Task Selector", version=0.1)
app.include_router(tasks_router)

Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
def startup_event() -> None:
    """Startup event"""
    settings = get_settings()
    logger.remove()
    logger.add(sys.stderr, level=settings.logger_level)
    task_buffer.check_connection()
    logger.debug("Started Satellite Task Selector App")
