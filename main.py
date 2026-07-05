from cli import Cli
from task_manager import TaskManager
from storage import Storage


if __name__ == "__main__":
    storage = Storage("tasks.json")
    manager = TaskManager(storage)
    cli_pannel = Cli(manager)
    
    cli_pannel.run()
