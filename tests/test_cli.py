from types import SimpleNamespace

import pytest

from lifelog.cli import Cli
from lifelog.exceptions import EmptyTextError, InvalidIndexError, TaskNotFoundError
from lifelog.log import Log
from lifelog.task import Task


class TaskManagerStub:
    def __init__(self, tasks=None, errors=None):
        self.tasks = tasks or []
        self.errors = errors or {}
        self.calls = []

    def add_task(self, title):
        self.calls.append(("add_task", title))
        error = self.errors.get("add_task")
        if error:
            raise error

    def rename_task(self, index, new_title):
        self.calls.append(("rename_task", index, new_title))
        error = self.errors.get("rename_task")
        if error:
            raise error

    def list_tasks(self):
        self.calls.append(("list_tasks",))
        return self.tasks

    def mark_task(self, index):
        self.calls.append(("mark_task", index))
        error = self.errors.get("mark_task")
        if error:
            raise error

    def delete_task(self, index):
        self.calls.append(("delete_task", index))
        error = self.errors.get("delete_task")
        if error:
            raise error


class LogManagerStub:
    def __init__(self, logs=None, errors=None):
        self.logs = logs or []
        self.errors = errors or {}
        self.calls = []

    def add_log(self, content):
        self.calls.append(("add_log", content))
        error = self.errors.get("add_log")
        if error:
            raise error

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


def test_rename_task_command_reports_success(capsys):
    task_manager = TaskManagerStub()
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="rt", index=1, new_title="updated"))
    assert capsys.readouterr().out == "Done.\n"
    assert task_manager.calls == [("rename_task", 1, "updated")]


def test_rename_task_command_prints_invalid_index_error(capsys):
    task_manager = TaskManagerStub(errors={"rename_task": InvalidIndexError()})
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="rt", index=2, new_title="ignored"))

    assert capsys.readouterr().out == "Invalid index.\n"


def test_rename_task_command_prints_empty_title_error(capsys):
    task_manager = TaskManagerStub(errors={"rename_task": EmptyTextError()})
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="rt", index=1, new_title="   "))

    assert capsys.readouterr().out == "Empty title.\n"


def test_list_tasks_command_formats_tasks(capsys):
    task_manager = TaskManagerStub(tasks=[Task("draft"), Task("done", completed=True)])
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="lt"))

    assert capsys.readouterr().out == "1 [ ] draft\n2 [*] done\n"


def test_mark_task_and_delete_task_commands(capsys):
    task_manager = TaskManagerStub()
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="mt", index=1))
    assert capsys.readouterr().out == "Done.\n"

    cli.run(SimpleNamespace(command="dt", index=2))
    assert capsys.readouterr().out == "Done.\n"

    assert task_manager.calls == [("mark_task", 1), ("delete_task", 2)]


def test_mark_task_command_prints_invalid_index_error(capsys):
    task_manager = TaskManagerStub(errors={"mark_task": InvalidIndexError()})
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="mt", index=0))

    assert capsys.readouterr().out == "Invalid index.\n"


def test_delete_task_command_prints_invalid_index_error(capsys):
    task_manager = TaskManagerStub(errors={"delete_task": InvalidIndexError()})
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="dt", index=0))

    assert capsys.readouterr().out == "Invalid index.\n"


def test_add_log_and_show_logs_commands(capsys):
    log_manager = LogManagerStub(logs=[Log("first", time="2026-07-11 10:00:00")])
    cli = Cli(TaskManagerStub(), log_manager)

    cli.run(SimpleNamespace(command="al", content="new log"))
    assert capsys.readouterr().out == "Done.\n"

    cli.run(SimpleNamespace(command="sl"))
    assert capsys.readouterr().out == "2026-07-11 10:00:00:\n\tfirst\n"
    assert log_manager.calls == [("add_log", "new log"), ("show_logs",)]


def test_add_task_command_prints_empty_title_error(capsys):
    task_manager = TaskManagerStub(errors={"add_task": EmptyTextError()})
    cli = Cli(task_manager, LogManagerStub())

    cli.run(SimpleNamespace(command="at", title="   "))

    assert capsys.readouterr().out == "Empty title.\n"


def test_add_log_command_prints_empty_content_error(capsys):
    log_manager = LogManagerStub(errors={"add_log": EmptyTextError()})
    cli = Cli(TaskManagerStub(), log_manager)

    cli.run(SimpleNamespace(command="al", content="   "))

    assert capsys.readouterr().out == "Empty content.\n"


@pytest.mark.parametrize("command", ["rt", "mt", "dt"])
def test_task_commands_report_missing_task(command, capsys):
    method_name = {"rt": "rename_task", "mt": "mark_task", "dt": "delete_task"}[command]
    task_manager = TaskManagerStub(errors={method_name: TaskNotFoundError()})
    cli = Cli(task_manager, LogManagerStub())
    args = {
        "rt": SimpleNamespace(command="rt", index=1, new_title="updated"),
        "mt": SimpleNamespace(command="mt", index=1),
        "dt": SimpleNamespace(command="dt", index=1),
    }[command]

    cli.run(args)

    assert capsys.readouterr().out == "Task not found.\n"
