from task import Task
import os
import json


class TaskManager:
    def __init__(self):
        self.filename = "tasks.json"

        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            with open(self.filename, "w") as t:
                json.dump([], t)

    def add_task(self, title):
        with open(self.filename, "r") as t:
            data = json.load(t)

        task = Task(title)
        data.append(task.to_dict())

        with open(self.filename, "w") as t:
            json.dump(data, t, indent=4)

    def show_list(self):
        with open(self.filename, "r") as t:
            data = json.load(t)

        tasks=[Task.from_dict(i) for i in data]
        return enumerate(tasks, start=1)
