from pathlib import Path

from lifelog.config import BASE_DIR, DATA_FILE


def test_data_file_is_in_project_root():
    project_root = Path(__file__).resolve().parent.parent

    assert BASE_DIR == project_root
    assert DATA_FILE == project_root / "data.json"
