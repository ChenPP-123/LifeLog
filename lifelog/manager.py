from .exceptions import EmptyTextError, InvalidIndexError


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title: str):
        if not title.strip():
            raise EmptyTextError()
        self.storage.task_add(title)

    def rename_task(self, index: int, new_title: str):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise InvalidIndexError()
        if not new_title.strip():
            raise EmptyTextError()
        target_id = data["tasks"][index - 1].id
        self.storage.task_rename(target_id, new_title)

    def list_tasks(self):
        return self.storage.load()["tasks"]

    def mark_task(self, index: int):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise InvalidIndexError()

        target_id = data["tasks"][index - 1].id
        self.storage.task_mark(target_id)

    def delete_task(self, index: int):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise InvalidIndexError()

        target_id = data["tasks"][index - 1].id
        self.storage.task_delete(target_id)


class LogManager:
    def __init__(self, storage):
        self.storage = storage

    def add_log(self, content: str):
        if not content.strip():
            raise EmptyTextError()

        self.storage.log_add(content)

    def show_logs(self):
        return self.storage.load()["logs"]
