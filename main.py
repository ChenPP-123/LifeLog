import sys
from task_manager import TaskManager

if __name__=="__main__":
    print("Welcome to LifeLog!\n")
    task_manager=TaskManager()

    while True:
        print("="*40)
        print("1. Add task\n2. List tasks\n3. Exit")
        print("="*40)
        
        inpu=int(input("Choose:"))
        print()
        match inpu:
            case 1:
                task_manager.add_task()
            case 2:
                task_manager.show_list()
            case 3:
                print("Good bye!")
                sys.exit(0)