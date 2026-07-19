import pytest

from lifelog.sqlite import Storage


@pytest.fixture
def storage(tmp_path):
    database = Storage(tmp_path / "lifelog.db")
    yield database
    database.close()
