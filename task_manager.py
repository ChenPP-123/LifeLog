from task import Task
import json
import os


class TaskManager:
    def __init__(self):
        self.file_name = "tasks.json"

        if not os.path.exists(self.file_name) or os.path.getsize(self.file_name) == 0:
            with open("tasks.json", "w") as t:
                json.dump([], t)

    def add_task(self, title):
        task = Task(title)

        with open(self.file_name, "r") as t:
            data = json.load(t)

        data.append({"title": task.title, "completed": task.completed})

        with open(self.file_name, "w") as t:
            json.dump(data, t, indent=4)

    def show_list(self):
        with open(self.file_name, "r") as t:
            data = json.load(t)

        return enumerate(data, start=1)
