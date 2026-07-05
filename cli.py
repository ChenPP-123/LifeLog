from task_manager import TaskManager
import sys
import os


class Cli:
    def __init__(self):
        self.task_manager = TaskManager()
        self.commands = {
            1: [self._show_menu, "Show menu"],
            2: [self._add_task, "Add task"],
            3: [self._list_tasks, "list_tasks"],
            4: [self._mark_task, "Finish/Unfinish task"],
            5: [self._delete, "Delete"],
            6: [self._exit, "Exit"],
        }

    def _show_menu(self):
        print("=" * 30)
        for i, j in self.commands.items():
            print(f"{i}. {j[-1]}")
        print("=" * 30)

    def _add_task(self):
        self.task_manager.add_task(title := input("Task title:\n"))
        print("Task added.")

    def _list_tasks(self):
        task_list = self.task_manager.list_tasks()
        for n, t in enumerate(task_list, start=1):
            print(f"{n}. {'[*]' if t.completed else '[ ]'} {t.title}")
        print()

    def _mark_task(self):
        index = int(input("Enter task index:"))
        self.task_manager.mark_task(index)
        print("Done.\n")

    def _delete(self):
        index = int(input("Enter task index:"))
        self.task_manager.delete_task(index)
        print("Deleted.\n")

    @staticmethod
    def _exit():
        print("Good bye!")
        sys.exit(0)

    def run(self):
        os.system("clear")
        print("Welcome to LifeLog!\n")

        self._show_menu()

        while True:
            inpu = int(input("Choose:"))
            self.commands.get(inpu)[0]()
