import json

from lifelog.storage import Storage
from lifelog.task import Task
from lifelog.log import Log


def test_storage_bootstraps_empty_file(tmp_path):
    path = tmp_path / "data.json"

    storage = Storage(str(path))

    assert json.loads(path.read_text()) == {"tasks": [], "logs": []}
    data = storage.load()
    assert data == {"tasks": [], "logs": []}


def test_storage_loads_models_from_json(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(
        json.dumps(
            {
                "tasks": [
                    {"title": "task 1", "completed": False},
                    {"title": "task 2", "completed": True},
                ],
                "logs": [
                    {"time": "2026-07-10 08:00:00", "content": "first"},
                    {"time": "2026-07-10 09:00:00", "content": "second"},
                ],
            }
        )
    )

    storage = Storage(str(path))
    data = storage.load()

    assert [task.title for task in data["tasks"]] == ["task 1", "task 2"]
    assert [task.completed for task in data["tasks"]] == [False, True]
    assert all(isinstance(task, Task) for task in data["tasks"])
    assert [log.content for log in data["logs"]] == ["first", "second"]
    assert all(isinstance(log, Log) for log in data["logs"])


def test_storage_saves_models_as_json(tmp_path):
    path = tmp_path / "data.json"
    storage = Storage(str(path))

    storage.save(
        {
            "tasks": [Task("task 1", completed=True)],
            "logs": [Log("saved log", time="2026-07-11 10:00:00")],
        }
    )

    assert json.loads(path.read_text()) == {
        "tasks": [{"title": "task 1", "completed": True}],
        "logs": [{"time": "2026-07-11 10:00:00", "content": "saved log"}],
    }
