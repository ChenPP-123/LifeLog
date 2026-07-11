import pytest

from lifelog.manager import TaskManager, LogManager
from lifelog.task import Task
from lifelog.log import Log
from fake_storage import FakeStorage


def init(data=None):
    storage = FakeStorage(data)
    task_manager = TaskManager(storage)
    log_manager = LogManager(storage)
    return storage, task_manager, log_manager


def test_add_task_persists_new_task():
    s, t, _ = init()
    t.add_task("task1")

    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 1


def test_rename_task_updates_selected_task():
    s, t, _ = init({"tasks": [Task("task1"), Task("task2")], "logs": []})

    assert t.rename_task(2, "tasknew2") is True
    assert [task.title for task in s.data["tasks"]] == ["task1", "tasknew2"]
    assert s.save_calls == 1


@pytest.mark.parametrize("index", [0, 3, -1])
def test_rename_task_rejects_invalid_index(index):
    s, t, _ = init({"tasks": [Task("task1")], "logs": []})

    assert t.rename_task(index, "ignored") is False
    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 0


def test_mark_task_flips_completion_state():
    s, t, _ = init({"tasks": [Task("task1"), Task("task2")], "logs": []})

    assert t.mark_task(2) is True
    assert s.data["tasks"][-1].completed is True
    assert s.save_calls == 1


@pytest.mark.parametrize("index", [0, 3, -1])
def test_mark_task_rejects_invalid_index(index):
    s, t, _ = init({"tasks": [Task("task1")], "logs": []})

    assert t.mark_task(index) is False
    assert s.data["tasks"][0].completed is False
    assert s.save_calls == 0


def test_delete_task_removes_selected_task():
    s, t, _ = init({"tasks": [Task("task1"), Task("task2")], "logs": []})

    assert t.delete_task(2) is True
    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 1


@pytest.mark.parametrize("index", [0, 3, -1])
def test_delete_task_rejects_invalid_index(index):
    s, t, _ = init({"tasks": [Task("task1")], "logs": []})

    assert t.delete_task(index) is False
    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 0


def test_list_tasks_returns_current_tasks():
    s, t, _ = init({"tasks": [Task("task1"), Task("task2", completed=True)], "logs": []})

    tasks = t.list_tasks()

    assert [task.title for task in tasks] == ["task1", "task2"]
    assert [task.completed for task in tasks] == [False, True]
    assert s.load_calls == 1


def test_add_log_persists_new_log():
    s, _, l = init()
    l.add_log("this is a test log")

    assert [log.content for log in s.data["logs"]] == ["this is a test log"]
    assert s.save_calls == 1


def test_show_logs_returns_current_logs():
    s, _, l = init(
        {
            "tasks": [],
            "logs": [Log("first", time="2026-07-10 08:00:00"), Log("second", time="2026-07-10 09:00:00")],
        }
    )

    logs = l.show_logs()

    assert [log.content for log in logs] == ["first", "second"]
    assert s.load_calls == 1
