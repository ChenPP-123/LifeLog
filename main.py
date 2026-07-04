import sys
import os
from task_manager import TaskManager


if __name__ == "__main__":
    os.system("clear")
    print("Welcome to LifeLog!\n")
    task_manager = TaskManager()

    print("=" * 30)
    print(
        "0. Show menu\n1. Add task\n2. List tasks\n3. Finish/Unfinish task\n4. Delete task\n5. Exit"
    )
    print("=" * 30)

    while True:
        match inpu := int(input("Choose:")):
            case 0:  # show menu
                print("=" * 30)
                print(
                    "0. Show menu\n1. Add task\n2. List tasks\n3. Mark task done\n4. Delete task\n5. Exit"
                )
                print("=" * 30)
            case 1:  # add task
                task_manager.add_task(title := input("Task title:\n"))
                print("Task added.\n")
            case 2:  # list tasks
                task_list = task_manager.list_tasks()
                for n, t in enumerate(task_list, start=1):
                    print(f"{n}. {'[*]' if t.completed else '[ ]'} {t.title}")
                print()
            case 3:  # Finish/Unfinish task 
                index = int(input("Enter task index:\n"))
                task_manager.mark_task(index)
                print("Done.\n")
            case 4:  # delete task
                index = int(input("Enter task index:\n"))
                task_manager.delete_task(index)
                print("Deleted.\n")
            case 5:  # exit
                print("Good bye!")
                sys.exit(0)
