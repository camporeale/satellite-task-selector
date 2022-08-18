"""Task Processor module"""
import abc
from typing import List
from loguru import logger

from app.models import Task


class TaskProcessor(abc.ABC):
    """Task Processor interface"""

    @abc.abstractmethod
    def process_batch(self, batch: List[Task]) -> None:
        """Processes a list of tasks"""


class SyncProcessor(TaskProcessor):
    """A syncronous processor"""

    def process_batch(self, batch: List[Task]) -> None:
        """Processes a list of tasks"""
        logger.debug(f"Batch processed succesfuly: {batch}")


class CeleryProcessor(TaskProcessor):
    """Celery Processor"""
