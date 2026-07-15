from datetime import datetime

import lifelog.log as log_module
from lifelog.log import Log


def test_log_round_trip_preserves_state():
    log = Log("test log", time="2026-07-10 12:30:45", id="log-1")

    data = log.to_dict()
    rebuilt = Log.from_dict(data)

    assert data == {
        "id": "log-1",
        "time": "2026-07-10 12:30:45",
        "content": "test log",
    }
    assert rebuilt.time == log.time
    assert rebuilt.content == log.content
    assert rebuilt.id == log.id


def test_log_loads_legacy_data_with_generated_id():
    log = Log.from_dict({"time": "2026-07-10 12:30:45", "content": "legacy log"})

    assert log.content == "legacy log"
    assert log.time == "2026-07-10 12:30:45"
    assert log.id


def test_log_uses_current_time_when_not_provided(monkeypatch):
    class FixedDatetime:
        @classmethod
        def now(cls):
            return datetime(2026, 7, 11, 12, 30, 45)

    monkeypatch.setattr(log_module, "datetime", FixedDatetime)

    log = Log("test log")

    assert log.time == "2026-07-11 12:30:45"
