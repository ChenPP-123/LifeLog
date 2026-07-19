import pytest

from lifelog.exceptions import EmptyTextError, TaskNotFoundError
from lifelog.manager import LogManager, TaskManager


def test_task_manager_manages_tasks(storage):
    manager = TaskManager(storage)

    manager.add_task("first")
    manager.add_task("second")
    manager.rename_task(2, "renamed")
    manager.mark_task(1)
    manager.delete_task(2)

    tasks = manager.list_tasks()
    assert [(task.title, task.completed) for task in tasks] == [("first", True)]


@pytest.mark.parametrize(
    "method,args",
    [("rename_task", (0, "name")), ("mark_task", (0,)), ("delete_task", (0,))],
)
def test_task_manager_rejects_missing_task(storage, method, args):
    manager = TaskManager(storage)

    with pytest.raises(TaskNotFoundError):
        getattr(manager, method)(*args)


@pytest.mark.parametrize(
    "method,args", [("add_task", ("  ",)), ("rename_task", (1, "  "))]
)
def test_task_manager_rejects_blank_titles(storage, method, args):
    manager = TaskManager(storage)

    with pytest.raises(EmptyTextError):
        getattr(manager, method)(*args)


def test_log_manager_manages_logs(storage):
    manager = LogManager(storage)

    manager.add_log("first log")

    assert [log.content for log in manager.show_logs()] == ["first log"]


def test_log_manager_rejects_blank_content(storage):
    with pytest.raises(EmptyTextError):
        LogManager(storage).add_log("  ")
