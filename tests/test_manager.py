from lifelog.manager import TaskManager, LogManager
from lifelog.task import Task
from lifelog.log import Log
from fake_storage import FakeStorage


def init():
    storage = FakeStorage()
    task_manager = TaskManager(storage)
    log_manager = LogManager(storage)
    return storage, task_manager, log_manager


def test_add_task():
    s, t, _ = init()
    t.add_task("task1")

    assert len(s.data["tasks"]) == 1
    assert type(s.data["tasks"][0]) is Task


def test_rename_task():
    s, t, _ = init()
    t.add_task("task1")
    t.add_task("task2")
    t.rename_task(2, "tasknew2")

    assert s.data["tasks"][-1].title == "tasknew2"


def test_delete_task():
    s, t, _ = init()
    t.add_task("task1")
    t.add_task("task2")
    t.delete_task(2)

    assert len(s.data["tasks"]) == 1


def test_mark_task():
    s, t, _ = init()
    t.add_task("task1")
    t.add_task("task2")
    t.mark_task(2)

    assert s.data["tasks"][-1].completed is True


def test_add_log():
    s, _, l = init()
    l.add_log("this is a test log")

    assert len(s.data["logs"]) == 1
    assert type(s.data["logs"][0]) is Log
