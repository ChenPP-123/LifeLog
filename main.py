import sys
from task_manager import TaskManager

if __name__ == "__main__":
    print("Welcome to LifeLog!\n")
    task_manager = TaskManager()

    while True:
        print("=" * 30)
        print("1. Add task\n2. List tasks\n3. Exit")
        print("=" * 30)

        inpu = int(input("Choose:"))
        print()
        match inpu:
            case 1:
                title = input("Task title:\n")
                task_manager.add_task(title)
                print("Task added.\n")
            case 2:
                task_list = task_manager.show_list()
                for n, t in task_list:
                    print(f"{n}. {t.title}")
                print()
            case 3:
                print("Good bye!")
                sys.exit(0)
