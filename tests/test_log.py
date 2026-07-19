from datetime import datetime

import lifelog.log as log_module
from lifelog.log import Log


def test_log_uses_provided_metadata():
    log = Log("test log", created_at="2026-07-10T12:30:45", id="log-1")

    assert (log.content, log.created_at, log.id) == (
        "test log",
        "2026-07-10T12:30:45",
        "log-1",
    )


def test_log_uses_current_time_when_not_provided(monkeypatch):
    class FixedDatetime:
        @classmethod
        def now(cls):
            return datetime(2026, 7, 11, 12, 30, 45)

    monkeypatch.setattr(log_module, "datetime", FixedDatetime)

    assert Log("test log").created_at == "2026-07-11T12:30:45"
