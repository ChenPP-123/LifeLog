import sys
import os


class Cli:
    def __init__(self, manager):
        self.manager = manager
        self.commands = {
            1: ("Show menu", self._show_menu),
            2: ("Add task", self._add_task),
            3: ("Rename task", self._rename_task),
            4: ("list_tasks", self._list_tasks),
            5: ("Finish/Unfinish task", self._mark_task),
            6: ("Delete", self._delete),
            7: ("Exit", self._exit),
        }

    def _show_menu(self):
        print("=" * 30)
        for i, (title, _) in self.commands.items():
            print(f"{i}. {title}")
        print("=" * 30)

    def _add_task(self):
        self.manager.add_task(title := input("Task title:\n"))
        print("Task added.\n")

    def _rename_task(self):
        while True:
            inpu = input("Enter task index:")
            try:
                inpu = int(inpu)
            except ValueError:
                print("Please input a number.")
                continue

            new_title = input("Enter the new title of the task:")
            if self.manager.rename_task(inpu, new_title):
                print("Done.\n")
                break

    def _list_tasks(self):
        task_list = self.manager.list_tasks()
        for n, t in enumerate(task_list, start=1):
            print(f"{n}. {'[*]' if t.completed else '[ ]'} {t.title}")
        print()

    def _mark_task(self):
        while True:
            index = input("Enter task index:")
            try:
                index = int(index)
            except ValueError:
                print("Please input a number.")
                continue

            if self.manager.mark_task(index):
                print("Done.\n")
                break
            else:
                print("Task not found.")

    def _delete(self):
        while True:
            index = input("Enter task index:")
            try:
                index = int(index)
            except ValueError:
                print("Please input a number.")
                continue

            if self.manager.delete_task(index):
                print("Deleted.\n")
                break
            else:
                print("Task not found.")

    @staticmethod
    def _exit():
        print("Good bye!")
        sys.exit()

    def run(self):
        os.system("clear")
        print("Welcome to LifeLog!\n")

        self._show_menu()

        while True:
            inpu = input("Choose:")
            try:
                inpu = int(inpu)
            except ValueError:
                print("Please input a number.")
                continue

            command = self.commands.get(inpu)
            if command:
                command[-1]()
            else:
                print("No such choice.")
