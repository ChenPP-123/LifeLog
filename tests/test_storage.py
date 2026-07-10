from lifelog.storage import Storage
from lifelog.task import Task
from lifelog.log import Log

storage = Storage("tests/fake_data.json")


def test_load():
    data = storage.load()

    assert type(data) is dict
    assert type(data["tasks"][0]) is Task
    assert len(data["tasks"]) == 2
    assert type(data["logs"][0]) is Log
    assert len(data["logs"]) == 3
