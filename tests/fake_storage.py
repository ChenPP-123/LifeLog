from copy import deepcopy

from lifelog.log import Log
from lifelog.task import Task


class FakeStorage:
    def __init__(self, data=None):
        self.data = deepcopy(data) if data is not None else {"tasks": [], "logs": []}
        self.load_calls = 0
        self.save_calls = 0
        self.saved_snapshots = []

    def load(self):
        self.load_calls += 1
        return self.data

    def save(self, data):
        self.save_calls += 1
        self.saved_snapshots.append(deepcopy(data))
        self.data = data

    def task_add(self, title):
        data = self.load()
        data["tasks"].append(Task(title))
        self.save(data)

    def task_rename(self, target_id, new_title):
        data = self.load()
        self._task_by_id(target_id).rename(new_title)
        self.save(data)

    def task_mark(self, target_id):
        data = self.load()
        self._task_by_id(target_id).change_status()
        self.save(data)

    def task_delete(self, target_id):
        data = self.load()
        data["tasks"].remove(self._task_by_id(target_id))
        self.save(data)

    def log_add(self, content):
        data = self.load()
        data["logs"].append(Log(content))
        self.save(data)

    def _task_by_id(self, target_id):
        for task in self.data["tasks"]:
            if task.id == target_id:
                return task
        raise KeyError(target_id)
