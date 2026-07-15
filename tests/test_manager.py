import pytest
from fake_storage import FakeStorage

from lifelog.log import Log
from lifelog.manager import (
    EMPTY_TEXT_ERROR,
    INVALID_INDEX_ERROR,
    LogManager,
    TaskManager,
)
from lifelog.task import Task


def init(data=None):
    storage = FakeStorage(data)
    task_manager = TaskManager(storage)
    log_manager = LogManager(storage)
    return storage, task_manager, log_manager


def test_add_task_persists_new_task():
    s, t, _ = init()
    t.add_task("task1")

    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.data["tasks"][0].id
    assert s.data["tasks"][0].created_at
    assert s.save_calls == 1


def test_add_task_rejects_blank_title():
    s, t, _ = init()

    with pytest.raises(ValueError, match=EMPTY_TEXT_ERROR):
        t.add_task("   ")

    assert s.data["tasks"] == []
    assert s.save_calls == 0


def test_rename_task_updates_selected_task():
    s, t, _ = init({"tasks": [Task("task1"), Task("task2")], "logs": []})

    t.rename_task(2, "tasknew2")
    assert [task.title for task in s.data["tasks"]] == ["task1", "tasknew2"]
    assert s.save_calls == 1


@pytest.mark.parametrize("index", [0, 3, -1])
def test_rename_task_rejects_invalid_index(index):
    s, t, _ = init({"tasks": [Task("task1")], "logs": []})

    with pytest.raises(ValueError, match=INVALID_INDEX_ERROR):
        t.rename_task(index, "ignored")

    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 0


def test_rename_task_rejects_blank_new_title():
    s, t, _ = init({"tasks": [Task("task1")], "logs": []})

    with pytest.raises(ValueError, match=EMPTY_TEXT_ERROR):
        t.rename_task(1, "  ")

    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 0


def test_mark_task_flips_completion_state():
    s, t, _ = init({"tasks": [Task("task1"), Task("task2")], "logs": []})

    t.mark_task(2)
    assert s.data["tasks"][-1].completed is True
    assert s.save_calls == 1


@pytest.mark.parametrize("index", [0, 3, -1])
def test_mark_task_rejects_invalid_index(index):
    s, t, _ = init({"tasks": [Task("task1")], "logs": []})

    with pytest.raises(ValueError, match=INVALID_INDEX_ERROR):
        t.mark_task(index)

    assert s.data["tasks"][0].completed is False
    assert s.save_calls == 0


def test_delete_task_removes_selected_task():
    s, t, _ = init({"tasks": [Task("task1"), Task("task2")], "logs": []})

    t.delete_task(2)
    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 1


@pytest.mark.parametrize("index", [0, 3, -1])
def test_delete_task_rejects_invalid_index(index):
    s, t, _ = init({"tasks": [Task("task1")], "logs": []})

    with pytest.raises(ValueError, match=INVALID_INDEX_ERROR):
        t.delete_task(index)

    assert [task.title for task in s.data["tasks"]] == ["task1"]
    assert s.save_calls == 0


def test_list_tasks_returns_current_tasks():
    s, t, _ = init(
        {
            "tasks": [Task("task1"), Task("task2", completed=True)],
            "logs": [],
        }
    )

    tasks = t.list_tasks()

    assert [task.title for task in tasks] == ["task1", "task2"]
    assert [task.completed for task in tasks] == [False, True]
    assert s.load_calls == 1


def test_add_log_persists_new_log():
    s, _, lm = init()
    lm.add_log("this is a test log")

    assert [log.content for log in s.data["logs"]] == ["this is a test log"]
    assert s.data["logs"][0].id
    assert s.data["logs"][0].time
    assert s.save_calls == 1


def test_add_log_rejects_blank_content():
    s, _, lm = init()

    with pytest.raises(ValueError, match=EMPTY_TEXT_ERROR):
        lm.add_log("   ")

    assert s.data["logs"] == []
    assert s.save_calls == 0


def test_show_logs_returns_current_logs():
    s, _, lm = init(
        {
            "tasks": [],
            "logs": [
                Log("first", time="2026-07-10 08:00:00"),
                Log("second", time="2026-07-10 09:00:00"),
            ],
        }
    )

    logs = lm.show_logs()

    assert [log.content for log in logs] == ["first", "second"]
    assert s.load_calls == 1
