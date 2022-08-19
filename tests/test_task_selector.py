from typing import List

import pytest  # pylint: disable=import-error

from app.models import BatchSelection, Task
from app.selector import MaxProfitBatchSelector

from tests.data import BATCHES, SELECTIONS


RESOURCES = ["disk", "proc", "camera"]


@pytest.mark.parametrize("batch, expected_selection", zip(BATCHES, SELECTIONS))
def test_task_selection(batch: List[Task], expected_selection: BatchSelection) -> None:
    """Test selector select method"""
    selector = MaxProfitBatchSelector()
    selection = selector.select_batch(batch)

    expected_tasks = {task.name for task in expected_selection.selected_tasks}
    expected_buffered = {task.name for task in expected_selection.buffered_tasks}
    assert {task.name for task in selection.selected_tasks} == expected_tasks
    assert {task.name for task in selection.buffered_tasks} == expected_buffered
    assert selection.profit == expected_selection.profit
