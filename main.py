import sys
import os
from task_manager import TaskManager

menu_list = [
    "Show menu",
    "Add task",
    "List tasks",
    "Finish/Unfinish task",
    "Delete task",
    "Exit",
]


def print_menu():
    print("=" * 30)
    for i, j in enumerate(menu_list, start=1):
        print(f"{i}. {j}")
    print("=" * 30)


def get_index_input(ls: list, discri: str) -> int:
    while True:
        try:
            inpu = int(input(f"{discri}:"))
            if not 1 <= inpu <= len(ls):
                raise ValueError
            else:
                break
        except ValueError:
            print("Invalid input. Try again.")
    return inpu


if __name__ == "__main__":
    os.system("clear")
    print("Welcome to LifeLog!\n")
    task_manager = TaskManager()

    print_menu()

    while True:
        inpu = get_index_input(menu_list, "Choose")
        match inpu:
            case 1:  # show menu
                print_menu()
            case 2:  # add task
                task_manager.add_task(title := input("Task title:\n"))
                print("Task added.\n")
            case 3:  # list tasks
                task_list = task_manager.list_tasks()
                for n, t in enumerate(task_list, start=1):
                    print(f"{n}. {'[*]' if t.completed else '[ ]'} {t.title}")
                print()
            case 4:  # Finish/Unfinish task
                index = get_index_input(task_manager.list_tasks(), "Enter task index")
                task_manager.mark_task(index)
                print("Done.\n")
            case 5:  # delete task
                index = get_index_input(task_manager.list_tasks(), "Enter task index")
                task_manager.delete_task(index)
                print("Deleted.\n")
            case 6:  # exit
                print("Good bye!")
                sys.exit(0)
