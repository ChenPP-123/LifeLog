from task import Task


class TaskManager:
    def __init__(self):
        self.task_list = []

    def show_list(self):
        return enumerate(self.task_list, start=1)

    def add_task(self, title):
        task = Task(title)
        self.task_list.append(task)
