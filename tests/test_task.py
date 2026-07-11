from lifelog.task import Task


def test_task_defaults_to_incomplete():
    task = Task("write tests")

    assert task.title == "write tests"
    assert task.completed is False


def test_task_round_trip_preserves_state():
    task = Task("write tests", completed=True)

    data = task.to_dict()
    rebuilt = Task.from_dict(data)

    assert data == {"title": "write tests", "completed": True}
    assert rebuilt.title == task.title
    assert rebuilt.completed is True


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
