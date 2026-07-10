from lifelog.log import Log


def test_to_dict():
    log = Log("test log")
    re = log.to_dict()

    assert type(re) is dict
    assert re["time"] == log.time
    assert re["content"] == log.content


def test_form_dict():
    data = {"time": "2026-7-10", "content": "test log"}
    log = Log.from_dict(data)

    assert type(log) is Log
