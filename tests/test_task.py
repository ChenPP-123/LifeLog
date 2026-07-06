from lifelog.task import Task


def test_todict():
    task_1 = Task("test_task")

    dict_1 = task_1.to_dict()

    assert type(dict_1) is dict
    assert dict_1["title"] == "test_task" and dict_1["completed"] is False


def test_from_dict():
    data = {"title": "test_task", "completed": True}

    task = Task.from_dict(data)

    assert type(task) is Task
