from lifelog.task import Task


def test_task_defaults_to_incomplete():
    task = Task("write tests")

    assert task.title == "write tests"
    assert task.completed is False
    assert task.id
    assert task.created_at


def test_task_uses_provided_metadata():
    task = Task(
        "write tests",
        completed=True,
        id="task-1",
        created_at="2026-07-10T12:30:45",
    )

    assert (task.title, task.completed, task.id, task.created_at) == (
        "write tests",
        True,
        "task-1",
        "2026-07-10T12:30:45",
    )


def test_task_can_be_renamed_and_completed():
    task = Task("old title")

    task.rename("new title")
    task.change_status()

    assert (task.title, task.completed) == ("new title", True)
