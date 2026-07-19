import argparse

from lifelog.cli import Cli
from lifelog.config import DATABASE_FILE
from lifelog.manager import LogManager, TaskManager
from lifelog.sqlite import Storage


def main():
    parser = argparse.ArgumentParser(
        prog="lifelog", description="A simple task manager"
    )
    subparser = parser.add_subparsers(dest="command", required=True)

    at = subparser.add_parser("at")
    at.add_argument("title")

    rt = subparser.add_parser("rt")
    rt.add_argument("index", type=int)
    rt.add_argument("new_title")

    subparser.add_parser("lt")

    mt = subparser.add_parser("mt")
    mt.add_argument("index", type=int)

    dt = subparser.add_parser("dt")
    dt.add_argument("index", type=int)

    al = subparser.add_parser("al")
    al.add_argument("content")

    subparser.add_parser("sl")

    args = parser.parse_args()

    with Storage(DATABASE_FILE) as storage:
        cli = Cli(TaskManager(storage), LogManager(storage))
        cli.run(args)


if __name__ == "__main__":
    main()
