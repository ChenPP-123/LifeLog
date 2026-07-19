from .exceptions import EmptyTextError


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title: str):
        if not title.strip():
            raise EmptyTextError()
        self.storage.add_task(title)

    def rename_task(self, index: int, new_title: str):
        if not new_title.strip():
            raise EmptyTextError()
        target_task = self.storage.get_task_by_index(index)
        self.storage.rename_task(new_title, target_task.id)

    def list_tasks(self):
        return self.storage.get_tasks()

    def mark_task(self, index: int):
        target_task = self.storage.get_task_by_index(index)
        target_task.change_status()
        self.storage.mark_task(target_task.completed, target_task.id)

    def delete_task(self, index: int):
        target_task = self.storage.get_task_by_index(index)
        self.storage.delete_task(target_task.id)


class LogManager:
    def __init__(self, storage):
        self.storage = storage

    def add_log(self, content: str):
        if not content.strip():
            raise EmptyTextError()

        self.storage.add_log(content)

    def show_logs(self):
        return self.storage.get_logs()
