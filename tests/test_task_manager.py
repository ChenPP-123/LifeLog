from task_manager import TaskManager
from tests.fake_storage import FakeStorage


def init():
    storage = FakeStorage()
    task_manger = TaskManager(storage)
    return storage, task_manger


def test_add_task():
    s, t = init()

    t.add_task("test_task_1")

    assert len(s.task_list) == 1
    assert s.task_list[0].title == "test_task_1"
    assert s.task_list[0].completed is False


def test_mark_task():
    s, t = init()

    t.add_task("task 1")
    t.mark_task(1)

    assert s.task_list[0].completed is True

    t.mark_task(1)

    assert s.task_list[0].completed is False


def test_delet_task():
    s, t = init()

    t.add_task("task 1")
    t.add_task("task 2")
    t.add_task("task 3")

    t.delete_task(2)

    assert len(s.task_list) == 2
    assert s.task_list[0].title == "task 1" and s.task_list[1].title == "task 3"


def test_rename_task():
    s, t = init()

    t.add_task("old name")
    t.rename_task(1, "new name")

    assert s.task_list[0].title == "new name"
