import pytest

from lifelog.exceptions import TaskNotFoundError
from lifelog.sqlite import SqlStorage


def test_storage_starts_with_no_records(storage):
    assert storage.get_tasks() == []
    assert storage.get_logs() == []


def test_storage_persists_tasks_and_logs(storage):
    storage.add_task("first task")
    storage.add_log("first log")

    task = storage.get_tasks()[0]
    log = storage.get_logs()[0]

    assert (task.title, task.completed) == ("first task", False)
    assert task.id
    assert task.created_at
    assert log.content == "first log"
    assert log.id
    assert log.created_at


def test_storage_persists_data_after_reopening(tmp_path):
    database_path = tmp_path / "lifelog.db"
    with SqlStorage(database_path) as storage:
        storage.add_task("saved task")
        storage.add_log("saved log")

    with SqlStorage(database_path) as storage:
        assert [task.title for task in storage.get_tasks()] == ["saved task"]
        assert [log.content for log in storage.get_logs()] == ["saved log"]


def test_storage_updates_and_deletes_tasks(storage):
    storage.add_task("first")
    storage.add_task("second")
    second_task = storage.get_task_by_index(2)

    storage.rename_task(second_task.id, "renamed")
    storage.mark_task(second_task.id, True)
    storage.delete_task(storage.get_task_by_index(1).id)

    tasks = storage.get_tasks()
    assert [(task.title, task.completed) for task in tasks] == [("renamed", True)]


@pytest.mark.parametrize("index", [0, -1, 1])
def test_get_task_by_index_rejects_missing_task(storage, index):
    with pytest.raises(TaskNotFoundError):
        storage.get_task_by_index(index)


@pytest.mark.parametrize(
    ("method", "args"),
    [
        ("rename_task", ("missing", "renamed")),
        ("mark_task", ("missing", True)),
        ("delete_task", ("missing",)),
    ],
)
def test_storage_rejects_unknown_task_id(storage, method, args):
    with pytest.raises(TaskNotFoundError):
        getattr(storage, method)(*args)
