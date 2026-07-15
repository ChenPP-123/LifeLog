from lifelog.task import Task


def test_task_defaults_to_incomplete():
    task = Task("write tests")

    assert task.title == "write tests"
    assert task.completed is False
    assert task.id
    assert task.created_at


def test_task_round_trip_preserves_state():
    task = Task(
        "write tests",
        completed=True,
        id="task-1",
        created_at="2026-07-10 12:30:45",
    )

    data = task.to_dict()
    rebuilt = Task.from_dict(data)

    assert data == {
        "id": "task-1",
        "title": "write tests",
        "completed": True,
        "created_at": "2026-07-10 12:30:45",
    }
    assert rebuilt.title == task.title
    assert rebuilt.completed is True
    assert rebuilt.id == task.id
    assert rebuilt.created_at == task.created_at


def test_task_loads_legacy_data_with_generated_metadata():
    task = Task.from_dict({"title": "legacy task", "completed": False})

    assert task.title == "legacy task"
    assert task.completed is False
    assert task.id
    assert task.created_at


def test_change_status_toggles_completion():
    task = Task("write tests")

    task.change_status()
    assert task.completed is True

    task.change_status()
    assert task.completed is False


def test_rename_updates_title():
    task = Task("old title")

    task.rename("new title")

    assert task.title == "new title"
