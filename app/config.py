"""Config module"""
import os
import logging

from pydantic import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Settings class"""

    redis_host: str = os.environ.get("REDIS_HOST", "redis")
    redis_port: int = int(os.environ.get("REDIS_PORT", "6379"))
    redis_db: int = int(os.environ.get("REDIS_DB", "0"))
    logger_level: str = os.environ.get("LOGGER_LEVEL", "DEBUG")
    log_file: str = os.environ.get("LOG_FILE", "/logs/api.log")


def get_settings() -> Settings:
    """Returns settings"""
    logger.info("Loading config settings from environment variables...")
    return Settings()
