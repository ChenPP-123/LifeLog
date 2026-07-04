from task import Task
from storage import Storage


class TaskManager:
    def __init__(self):
        self.storage = Storage()

    def add_task(self, title):
        data = self.storage.load()

        task = Task(title)
        data.append(task)

        self.storage.save(data)

    def list_tasks(self):
        return self.storage.load()
