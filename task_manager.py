from task import Task


class TaskManager:
    def __init__(self):
        self.taskList = []

    def show_list(self):
        for n, t in enumerate(self.taskList, start=1):
            print(f"{n}. {t.title}")
            print()

    def add_task(self):
        inpu = input("Task title:\n")
        task = Task(inpu)
        self.taskList.append(task)
        print("Task added.\n")
