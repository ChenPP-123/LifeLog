from lifelog.task import Task


def test_to_dict():
    task = Task("this is a test task")
    re = task.to_dict()

    assert type(re) is dict
    assert re["title"] == task.title
    assert re["completed"] is False


def test_from_dict():
    data = {"title": "test task", "completed": False}
    task = Task.from_dict(data)

    assert type(task) is Task
