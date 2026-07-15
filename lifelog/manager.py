INVALID_INDEX_ERROR = "invalid_index"
EMPTY_TEXT_ERROR = "empty_text"


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title: str):
        if not title.strip():
            raise ValueError(EMPTY_TEXT_ERROR)
        self.storage.task_add(title)

    def rename_task(self, index: int, new_title: str):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise ValueError(INVALID_INDEX_ERROR)
        if not new_title.strip():
            raise ValueError(EMPTY_TEXT_ERROR)
        target_id = data["tasks"][index - 1].id
        self.storage.task_rename(target_id, new_title)

    def list_tasks(self):
        return self.storage.load()["tasks"]

    def mark_task(self, index: int):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise ValueError(INVALID_INDEX_ERROR)

        target_id = data["tasks"][index - 1].id
        self.storage.task_mark(target_id)

    def delete_task(self, index: int):
        data = self.storage.load()
        if not 1 <= index <= len(data["tasks"]):
            raise ValueError(INVALID_INDEX_ERROR)

        target_id = data["tasks"][index - 1].id
        self.storage.task_delete(target_id)


class LogManager:
    def __init__(self, storage):
        self.storage = storage

    def add_log(self, content: str):
        if not content.strip():
            raise ValueError(EMPTY_TEXT_ERROR)

        self.storage.log_add(content)

    def show_logs(self):
        return self.storage.load()["logs"]
