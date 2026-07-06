from .task import Task


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title):
        data = self.storage.load()
        task = Task(title)
        data.append(task)
        self.storage.save(data)

    def rename_task(self, index, new_title):
        data = self.storage.load()
        if 1 <= index <= len(data):
            data[index - 1].rename(new_title)
            self.storage.save(data)
            return True
        else:
            return False

    def list_tasks(self):
        return self.storage.load()

    def mark_task(self, index):
        data = self.storage.load()
        if 1 <= index <= len(data):
            data[index - 1].change_status()
            self.storage.save(data)
            return True
        else:
            return False

    def delete_task(self, index):
        data = self.storage.load()
        if 1 <= index <= len(data):
            del data[index - 1]
            self.storage.save(data)
            return True
        else:
            return False
