"""Routers module"""
from typing import List

from fastapi import APIRouter
from loguru import logger

from app.buffer import task_buffer
from app.models import BatchSelection, Task
from app.processor import SyncProcessor
from app.selector import MaxProfitBatchSelector


tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post("/batch", response_model=BatchSelection)
def add_batch(batch: List[Task]):
    """Receives a list of tasks, combines them with buffered tasks from previous
    requests, selects the subset with the higher profit, sends them for processing,
    and buffers the unselected tasks
    """
    logger.info(f"Processing new batch, task list: {[t.name for t in batch]}")
    selector = MaxProfitBatchSelector()
    processor = SyncProcessor()
    buffered_tasks = task_buffer.get_tasks()
    batch.extend(buffered_tasks)
    batch_selection = selector.select_batch(batch)
    task_buffer.save_tasks(batch_selection.buffered_tasks)
    task_buffer.delete_tasks([task for task in batch_selection.selected_tasks if task.buffered])
    processor.process_batch(batch_selection.selected_tasks)
    return batch_selection
