import argparse


from lifelog.manager import TaskManager
from lifelog.storage import Storage


def _add(manager, args):
    manager.add_task(args.title)


def _rename(manager, args):
    manager.rename_task(args.index, args.title)


def _list(manager, args):
    manager.list_tasks()


def _mark(manager, args):
    manager.mark_task(args.index)


def _delete(manager, args):
    manager.delete_task(args.index)


commands = {
    "add": _add,
    "rename": _rename,
    "list": _list,
    "mark": _mark,
    "delete": _delete,
}


def main():
    storage = Storage("tasks.json")
    manager = TaskManager(storage)

    parser = argparse.ArgumentParser(
        prog="lifelog", description="A simple task manager"
    )
    subparser = parser.add_subparsers(dest="command", required=True)

    add = subparser.add_parser("add")
    add.add_argument("title")

    rename = subparser.add_parser("rename")
    rename.add_argument("index", type=int)
    rename.add_argument("title")

    subparser.add_parser("list")

    mark = subparser.add_parser("mark")
    mark.add_argument("index", type=int)

    delete = subparser.add_parser("delete")
    delete.add_argument("index", type=int)

    args = parser.parse_args()

    command = commands.get(args.command)
    if command:
        command(manager, args)


if __name__ == "__main__":
    main()
