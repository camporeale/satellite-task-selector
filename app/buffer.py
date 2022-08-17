"""Task buffer module"""
import abc
from typing import List

import redis
from redis import RedisError
from loguru import logger

from app.config import get_settings
from app.exceptions import TaskBufferException
from app.models import Task


class TaskBuffer(abc.ABC):
    """Task buffer interface"""
    @abc.abstractmethod
    def check_connection(self) -> None:
        """Checks the connections is ok"""

    @abc.abstractmethod
    def get_tasks(self) -> List[Task]:
        """Return a list of buffered tasks

        Returns:
            task_list: a list of tasks
        """

    @abc.abstractmethod
    def delete_tasks(self, task_list: List[Task]) -> None:
        """Delete a list from buffer

        Args:
            task_list: a list of tasks
        """

    @abc.abstractmethod
    def save_tasks(self, task_list: List[Task]):
        """Save tasks to buffer

        Args:
            task_list: a list of tasks
        """


class RedisBuffer(TaskBuffer):
    """A redis based task buffer implementation"""
    TASK_PREFIX = "satellite:task:"

    def __init__(self, connection: redis.Redis) -> None:
        """Class constructor

        Args:
            connection: an instance of Redis
        """
        self._connection = connection

    def check_connection(self) -> None:
        """Checks the connections is ok

        Raises:
            TaskBufferException if unable to connect to the redis instance
        """
        try:
            if not self._connection.ping():
                raise TaskBufferException("Failed to connect to Redis")
        except RedisError as excp:
            logger.exception(excp)
            raise TaskBufferException("Failed to connect to buffer") from excp

    def get_tasks(self) -> List[Task]:
        """Return a list of buffered tasks

        Returns:
            task_list: a list of tasks
        """
        try:
            all_tasks_keys = self._connection.keys(self.TASK_PREFIX + "*")
            tasks = self._connection.mget(all_tasks_keys)
        except RedisError as excp:
            logger.exception(excp)
            raise TaskBufferException("Failed to get tasks from buffer") from excp
        return [Task.parse_raw(task) for task in tasks]

    def delete_tasks(self, task_list: List[Task]) -> None:
        """Delete a list from buffer

        Args:
            task_list: a list of tasks
        """
        try:
            pipe = self._connection.pipeline()
            for task in task_list:
                pipe.delete(self.TASK_PREFIX+task.name)
            pipe.execute()
        except RedisError as excp:
            logger.exception(excp)
            raise TaskBufferException("Failed to delete tasks in buffer") from excp

    def save_tasks(self, task_list: List[Task]) -> None:
        """Save tasks to buffer
        Args:
            task_list: a list of tasks
        """
        try:
            pipe = self._connection.pipeline()
            for task in task_list:
                task.buffered = True
                pipe.set(self.TASK_PREFIX + task.name, task.json())
            result = pipe.execute()
            if not all(result):
                failed_count = len(result) - sum(result)
                failure_message = f"Failed to load tasks to buffer, number of failed loads: {failed_count}"
                logger.error(failure_message)
        except RedisError as excp:
            logger.exception(excp)
            raise TaskBufferException("Failed to save tasks to buffer") from excp

def create_buffer() -> TaskBuffer:
    """Returns a buffer"""
    configuration = get_settings()
    connection = redis.Redis(
        host=configuration.redis_host,
        port=configuration.redis_port,
        db=configuration.redis_db,
        decode_responses=True
    )
    return RedisBuffer(connection=connection)


task_buffer = create_buffer()
