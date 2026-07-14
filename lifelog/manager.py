from .log import Log
from .task import Task

INVALID_INDEX_ERROR = "invalid_index"
EMPTY_TEXT_ERROR = "empty_text"


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title: str):
        if not title.strip():
            raise ValueError(EMPTY_TEXT_ERROR)

        data = self.storage.load()
        task = Task(title)
        data["tasks"].append(task)
        self.storage.save(data)

    def rename_task(self, index: int, new_title: str):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise ValueError(INVALID_INDEX_ERROR)
        if not new_title.strip():
            raise ValueError(EMPTY_TEXT_ERROR)

        data["tasks"][index - 1].rename(new_title)
        self.storage.save(data)

    def list_tasks(self):
        return self.storage.load()["tasks"]

    def mark_task(self, index: int):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise ValueError(INVALID_INDEX_ERROR)

        data["tasks"][index - 1].change_status()
        self.storage.save(data)

    def delete_task(self, index: int):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise ValueError(INVALID_INDEX_ERROR)

        del data["tasks"][index - 1]
        self.storage.save(data)


class LogManager:
    def __init__(self, storage):
        self.storage = storage

    def add_log(self, content: str):
        if not content.strip():
            raise ValueError(EMPTY_TEXT_ERROR)

        data = self.storage.load()
        log = Log(content)
        data["logs"].append(log)
        self.storage.save(data)

    def show_logs(self):
        return self.storage.load()["logs"]
