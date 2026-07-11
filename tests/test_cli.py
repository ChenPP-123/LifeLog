from types import SimpleNamespace

from lifelog.cli import Cli
from lifelog.log import Log
from lifelog.task import Task


class TaskManagerStub:
    def __init__(self, tasks=None):
        self.tasks = tasks or []
        self.calls = []

    def add_task(self, title):
        self.calls.append(("add_task", title))

    def rename_task(self, index, new_title):
        self.calls.append(("rename_task", index, new_title))
        return index == 1

    def list_tasks(self):
        self.calls.append(("list_tasks",))
        return self.tasks

    def mark_task(self, index):
        self.calls.append(("mark_task", index))
        return index == 1

    def delete_task(self, index):
        self.calls.append(("delete_task", index))
        return index == 1


class LogManagerStub:
    def __init__(self, logs=None):
        self.logs = logs or []
        self.calls = []

    def add_log(self, content):
        self.calls.append(("add_log", content))

    def show_logs(self):
        self.calls.append(("show_logs",))
        return self.logs


def test_unknown_command_does_nothing(capsys):
    cli = Cli(TaskManagerStub(), LogManagerStub())

    cli.run(SimpleNamespace(command="unknown"))

    assert capsys.readouterr().out == ""


def test_add_task_command_prints_done(capsys):
    task_manager = TaskManagerStub()
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="at", title="write tests"))

    assert task_manager.calls == [("add_task", "write tests")]
    assert capsys.readouterr().out == "Done.\n"


def test_rename_task_command_reports_success_and_failure(capsys):
    task_manager = TaskManagerStub()
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="rt", index=1, new_title="updated"))
    assert capsys.readouterr().out == "Done.\n"

    cli.run(SimpleNamespace(command="rt", index=2, new_title="ignored"))
    assert capsys.readouterr().out == "No such task.\n"
    assert task_manager.calls == [("rename_task", 1, "updated"), ("rename_task", 2, "ignored")]


def test_list_tasks_command_formats_tasks(capsys):
    task_manager = TaskManagerStub(tasks=[Task("draft"), Task("done", completed=True)])
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="lt"))

    assert capsys.readouterr().out == "1 [ ] draft\n2 [*] done\n\n"


def test_mark_task_and_delete_task_commands(capsys):
    task_manager = TaskManagerStub()
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="mt", index=1))
    assert capsys.readouterr().out == "Done.\n"

    cli.run(SimpleNamespace(command="dt", index=2))
    assert capsys.readouterr().out == "No such task.\n"

    assert task_manager.calls == [("mark_task", 1), ("delete_task", 2)]


def test_add_log_and_show_logs_commands(capsys):
    log_manager = LogManagerStub(logs=[Log("first", time="2026-07-11 10:00:00")])
    cli = Cli(TaskManagerStub(), log_manager)

    cli.run(SimpleNamespace(command="al", content="new log"))
    assert capsys.readouterr().out == "Done.\n"

    cli.run(SimpleNamespace(command="sl"))
    assert capsys.readouterr().out == "2026-07-11 10:00:00:\n\tfirst\n"
    assert log_manager.calls == [("add_log", "new log"), ("show_logs",)]
