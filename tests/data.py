from app.models import Task, BatchSelection


T1 = Task(name="t1", resources=["proc"], profit=2.1)
T2 = Task(name="t2", resources=["proc", "disk"], profit=0.8)
T3 = Task(name="t3", resources=["proc", "disk", "camera"], profit=3.2)
T4 = Task(name="t4", resources=["disk", "camera"], profit=2.3)
T5 = Task(name="t5", resources=["proc"], profit=3.1)
T6 = Task(name="t6", resources=["disk"], profit=1.1)

TASK_LIST_1 = [T1, T3, T4]
TASK_LIST_1_SELECTION = BatchSelection(selected_tasks=[T1, T4], buffered_tasks=[T3], profit=4.4)

TASK_LIST_2 = [T1, T2, T3]
TASK_LIST_2_SELECTION = BatchSelection(selected_tasks=[T3], buffered_tasks=[T1, T2], profit=3.2)

TASK_LIST_3 = [T1, T2, T3, T4, T5]
TASK_LIST_3_SELECTION = BatchSelection(
    selected_tasks=[T4, T5], buffered_tasks=[T1, T2, T3], profit=5.4
)

TASK_LIST_4 = [T1, T2, T6]
TASK_LIST_4_SELECTION = BatchSelection(selected_tasks=[T1, T6], buffered_tasks=[T2], profit=3.2)

BATCHES = [TASK_LIST_1, TASK_LIST_2, TASK_LIST_3, TASK_LIST_4]
SELECTIONS = [
    TASK_LIST_1_SELECTION,
    TASK_LIST_2_SELECTION,
    TASK_LIST_3_SELECTION,
    TASK_LIST_4_SELECTION,
]
