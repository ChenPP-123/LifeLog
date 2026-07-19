import sqlite3
from pathlib import Path

from .exceptions import TaskNotFoundError
from .log import Log
from .task import Task


class Storage:
    def __init__(self, database_path: str | Path):
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.connection.close()

    def _create_tables(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def get_task_by_index(self, index):
        if index < 1:
            raise TaskNotFoundError()
        row = self.connection.execute(
            """
            SELECT id, title, completed, created_at
            FROM tasks
            ORDER BY created_at, id
            LIMIT 1 OFFSET ?
            """,
            (index - 1,),
        ).fetchone()
        if row is None:
            raise TaskNotFoundError()
        return self._task_from_row(row)

    def add_task(self, title):
        task = Task(title)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO tasks (id, title, completed, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (task.id, task.title, task.completed, task.created_at),
            )

    def get_tasks(self):
        rows = self.connection.execute(
            """
            SELECT id, title, completed, created_at
            FROM tasks
            ORDER BY created_at, id
            """
        ).fetchall()
        return [self._task_from_row(row) for row in rows]

    def rename_task(self, target_id, new_title):
        with self.connection:
            result = self.connection.execute(
                "UPDATE tasks SET title = ? WHERE id = ?", (new_title, target_id)
            )
        if result.rowcount == 0:
            raise TaskNotFoundError()

    def mark_task(self, target_id, completed):
        with self.connection:
            result = self.connection.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?",
                (int(completed), target_id),
            )
        if result.rowcount == 0:
            raise TaskNotFoundError()

    def delete_task(self, target_id):
        with self.connection:
            result = self.connection.execute(
                "DELETE FROM tasks WHERE id = ?", (target_id,)
            )
        if result.rowcount == 0:
            raise TaskNotFoundError()

    def add_log(self, content):
        log = Log(content)
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO logs (id, content, created_at)
                VALUES (?, ?, ?)
                """,
                (log.id, log.content, log.created_at),
            )

    def get_logs(self):
        rows = self.connection.execute(
            """
            SELECT id, content, created_at
            FROM logs
            ORDER BY created_at, id
            """
        ).fetchall()
        return [self._log_from_row(row) for row in rows]

    @staticmethod
    def _task_from_row(row):
        return Task(row["title"], bool(row["completed"]), row["id"], row["created_at"])

    @staticmethod
    def _log_from_row(row):
        return Log(row["content"], row["created_at"], row["id"])
