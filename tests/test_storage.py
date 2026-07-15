import json

import pytest

from lifelog.exceptions import TaskNotFoundError
from lifelog.log import Log
from lifelog.storage import Storage
from lifelog.task import Task


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
                    {
                        "id": "task-1",
                        "title": "task 1",
                        "completed": False,
                        "created_at": "2026-07-10 08:00:00",
                    },
                    {
                        "id": "task-2",
                        "title": "task 2",
                        "completed": True,
                        "created_at": "2026-07-10 09:00:00",
                    },
                ],
                "logs": [
                    {"id": "log-1", "time": "2026-07-10 08:00:00", "content": "first"},
                    {"id": "log-2", "time": "2026-07-10 09:00:00", "content": "second"},
                ],
            }
        )
    )

    storage = Storage(str(path))
    data = storage.load()

    assert [task.title for task in data["tasks"]] == ["task 1", "task 2"]
    assert [task.completed for task in data["tasks"]] == [False, True]
    assert [task.id for task in data["tasks"]] == ["task-1", "task-2"]
    assert [task.created_at for task in data["tasks"]] == [
        "2026-07-10 08:00:00",
        "2026-07-10 09:00:00",
    ]
    assert all(isinstance(task, Task) for task in data["tasks"])
    assert [log.content for log in data["logs"]] == ["first", "second"]
    assert [log.id for log in data["logs"]] == ["log-1", "log-2"]
    assert all(isinstance(log, Log) for log in data["logs"])


def test_storage_saves_models_as_json(tmp_path):
    path = tmp_path / "data.json"
    storage = Storage(str(path))

    storage.save(
        {
            "tasks": [
                Task(
                    "task 1",
                    completed=True,
                    id="task-1",
                    created_at="2026-07-11 09:00:00",
                )
            ],
            "logs": [Log("saved log", time="2026-07-11 10:00:00", id="log-1")],
        }
    )

    assert json.loads(path.read_text()) == {
        "tasks": [
            {
                "id": "task-1",
                "title": "task 1",
                "completed": True,
                "created_at": "2026-07-11 09:00:00",
            }
        ],
        "logs": [
            {
                "id": "log-1",
                "time": "2026-07-11 10:00:00",
                "content": "saved log",
            }
        ],
    }


def test_storage_updates_and_deletes_tasks_by_id(tmp_path):
    path = tmp_path / "data.json"
    storage = Storage(str(path))
    storage.save(
        {
            "tasks": [
                Task("first", id="task-1"),
                Task("second", id="task-2"),
            ],
            "logs": [],
        }
    )

    storage.task_rename("task-2", "renamed")
    storage.task_mark("task-2")
    storage.task_delete("task-1")

    tasks = storage.load()["tasks"]
    assert [(task.id, task.title, task.completed) for task in tasks] == [
        ("task-2", "renamed", True)
    ]


@pytest.mark.parametrize(
    ("method", "args"),
    [
        ("task_rename", ("missing", "renamed")),
        ("task_mark", ("missing",)),
        ("task_delete", ("missing",)),
    ],
)
def test_storage_rejects_unknown_task_id(tmp_path, method, args):
    storage = Storage(str(tmp_path / "data.json"))

    with pytest.raises(TaskNotFoundError):
        getattr(storage, method)(*args)
