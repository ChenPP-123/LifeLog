import pytest

from lifelog.sqlite import SqlStorage


@pytest.fixture
def storage(tmp_path):
    database = SqlStorage(tmp_path / "lifelog.db")
    yield database
    database.close()
