from task import Task
import json
import os


class Storage:
    def __init__(self):
        self.filename = "tasks.json"

        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            with open(self.filename, "w") as t:
                json.dump([], t)

    def load(self):
        with open(self.filename, "r") as t:
            return [Task.from_dict(i) for i in json.load(t)]

    def save(self, data):
        with open(self.filename, "w") as t:
            tasks = [i.to_dict() for i in data]
            json.dump(tasks, t, indent=4)