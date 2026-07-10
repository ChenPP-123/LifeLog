from .task import Task
from .log import Log


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title: str):
        data = self.storage.load()
        task = Task(title)
        data["tasks"].append(task)
        self.storage.save(data)

    def rename_task(self, index: int, new_title: str):
        data = self.storage.load()
        if 1 <= index <= len(data["tasks"]):
            data["tasks"][index - 1].rename(new_title)
            self.storage.save(data)
            return True
        else:
            return False

    def list_tasks(self):
        return self.storage.load()["tasks"]

    def mark_task(self, index: int):
        data = self.storage.load()
        if 1 <= index <= len(data["tasks"]):
            data["tasks"][index - 1].change_status()
            self.storage.save(data)
            return True
        else:
            return False

    def delete_task(self, index: int):
        data = self.storage.load()
        if 1 <= index <= len(data["tasks"]):
            del data["tasks"][index - 1]
            self.storage.save(data)
            return True
        else:
            return False


class LogManager:
    def __init__(self, storage):
        self.storage = storage

    def add_log(self, content: str):
        data = self.storage.load()
        log = Log(content)
        data["logs"].append(log)
        self.storage.save(data)

    def show_log(self):
        return self.storage.load()["logs"]
