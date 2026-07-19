from pathlib import Path

from lifelog.config import BASE_DIR, DATABASE_FILE


def test_database_file_is_in_project_root():
    project_root = Path(__file__).resolve().parent.parent

    assert BASE_DIR == project_root
    assert DATABASE_FILE == project_root / "lifelog.db"
