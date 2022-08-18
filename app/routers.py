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
def add_batch(batch: List[Task]) -> BatchSelection:
    """Receives a list of tasks, combines them with buffered tasks from previous
    requests, selects the subset with the higher profit, sends them for processing,
    and buffers the unselected tasks
    """
    logger.info(f"Processing new batch, task list: {[t.name for t in batch]}")
    selector = MaxProfitBatchSelector()
    processor = SyncProcessor()

    # Create batch from new tasks and buffered tasks
    buffered_tasks = task_buffer.get_tasks()
    batch.extend(buffered_tasks)

    # Select batch to process
    batch_selection = selector.select_batch(batch)

    # Save to buffer new tasks not selected to be processed
    if batch_selection.buffered_tasks:
        task_buffer.save_tasks(batch_selection.buffered_tasks)

    # Delete from buffer selected tasks previously buffered
    unbuffered = [task for task in batch_selection.selected_tasks if task.buffered]
    if unbuffered:
        task_buffer.delete_tasks(unbuffered)

    processor.process_batch(batch_selection.selected_tasks)
    return batch_selection
