from .manager import EMPTY_TEXT_ERROR, INVALID_INDEX_ERROR


class Cli:
    def __init__(self, task_manager, log_manager):
        self.task_manager = task_manager
        self.log_manager = log_manager
        self.commands = {
            "at": self._add_task,
            "rt": self._rename_task,
            "lt": self._list_tasks,
            "mt": self._mark_task,
            "dt": self._delete_task,
            "al": self._add_log,
            "sl": self._show_logs,
        }

    def run(self, args):
        command = self.commands.get(args.command)
        if command:
            command(args)

    def _add_task(self, args):
        try:
            self.task_manager.add_task(args.title)
            print("Done.")
        except ValueError as error:
            if str(error) == EMPTY_TEXT_ERROR:
                print("Empty title.")
            else:
                raise

    def _rename_task(self, args):
        try:
            self.task_manager.rename_task(args.index, args.new_title)
            print("Done.")
        except ValueError as error:
            if str(error) == INVALID_INDEX_ERROR:
                print("Invalid index.")
            elif str(error) == EMPTY_TEXT_ERROR:
                print("Empty title.")
            else:
                raise

    def _list_tasks(self, args):
        for i, t in enumerate(self.task_manager.list_tasks(), start=1):
            print(f"{i} {'[ ]' if t.completed is False else '[*]'} {t.title}")
        print()

    def _mark_task(self, args):
        try:
            self.task_manager.mark_task(args.index)
            print("Done.")
        except ValueError as error:
            if str(error) == INVALID_INDEX_ERROR:
                print("Invalid index.")
            else:
                raise

    def _delete_task(self, args):
        try:
            self.task_manager.delete_task(args.index)
            print("Done.")
        except ValueError as error:
            if str(error) == INVALID_INDEX_ERROR:
                print("Invalid index.")
            else:
                raise

    def _add_log(self, args):
        try:
            self.log_manager.add_log(args.content)
            print("Done.")
        except ValueError as error:
            if str(error) == EMPTY_TEXT_ERROR:
                print("Empty log content.")
            else:
                raise

    def _show_logs(self, args):
        for log in self.log_manager.show_logs():
            print(f"{log.time}:\n\t{log.content}")
