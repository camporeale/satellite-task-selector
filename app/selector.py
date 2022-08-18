"""BatchSelector module"""
import abc
import sys
import logging
from typing import List
from app.models import BatchSelection, Task

logger = logging.getLogger(__name__)


class BatchSelectorInterface(abc.ABC):
    """BatchSelector interface"""

    @abc.abstractmethod
    def select_batch(self, task_list: List[Task]) -> BatchSelection:
        """Takes a list of tasks and makes a batch selection"""


class MaxProfitBatchSelector(BatchSelectorInterface):
    """Batch Selector that uses profit maximization as a selection"""

    def select_batch(self, task_list: List[Task]) -> BatchSelection:
        """
        Takes a list of tasks and makes a batch selection based on
        the maximum profit combination

        Args:
            task_list: a list of tasks
        Returns
            a subset of the task list
        """
        final_selection = BatchSelection(
            selected_tasks=[], buffered_tasks=[], profit=sys.float_info.min
        )

        # Sort list of tasks by higher profit
        task_list.sort(key=lambda x: x.profit, reverse=True)  # type:ignore

        # iterate on all tasks
        for idx, task in enumerate(task_list):
            commited_resources = task.resources
            task_selection = BatchSelection(
                selected_tasks=[task], buffered_tasks=[], profit=task.profit
            )
            start_idx = idx + 1
            for other_task in task_list[start_idx:]:
                if commited_resources.isdisjoint(other_task.resources):
                    task_selection.selected_tasks.append(other_task)
                    task_selection.profit += other_task.profit
                    commited_resources = commited_resources.union(other_task.resources)

            if task_selection.profit > final_selection.profit:
                final_selection = task_selection

        selected_tasks = [task.name for task in final_selection.selected_tasks]
        final_selection.buffered_tasks = [
            task for task in task_list if task.name not in selected_tasks
        ]

        return final_selection
