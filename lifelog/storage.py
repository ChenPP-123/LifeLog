import json
import os
import sqlite3

from .exceptions import TaskNotFoundError
from .log import Log
from .task import Task


class Storage:
    def __init__(self, filename: str, db_path):
        self.filename = filename
        self.MODEL_MAP = {"tasks": Task, "logs": Log}

        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            with open(self.filename, "w") as d:
                json.dump({"tasks": [], "logs": []}, d, indent=4)

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        sql = """
CREATE TABLE IF NOT EXISTS tasks (
id TEXT PRIMARY KEY,
title TEXT NOT NULL,
completed INTEGER NOT NULL,
created_at TEXT NOT NULL)
"""
        self.cursor.execute(sql)
        self.conn.commit()

    def get_task_by_index(self, index):
        sql = """
SELECT * FROM tasks ORDER BY created_at
LIMIT 1 OFFSET ?
"""
        self.cursor.execute(sql, (index,))
        row = self.cursor.fetchone()
        if row is None:
            raise TaskNotFoundError()
        return Task.from_sql_row(row)

    def add_task(self, title):
        task = Task(title)
        sql = """
INSERT INTO tasks (id, title, completed, created_at)
VALUES (?, ?, ?, ?)
"""
        self.cursor.execute(sql, (task.id, task.title, task.completed, task.created_at))
        self.conn.commit()

    def get_tasks(self):
        sql = """
SELECT id, title, completed, created_at
FROM tasks
"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [Task.from_sql_row(i) for i in rows]

    def rename_task(self, new_title, target_id):
        sql = """
UPDATE tasks
SET title=?
WHERE id=?
"""
        self.cursor.execute(sql, (new_title, target_id))
        self.conn.commit()

    def mark_task(self, new_completed, target_id):
        sql = """
UPDATE tasks
SET completed=?
WHERE id=?
"""
        self.cursor.execute(sql, (int(new_completed), target_id))
        self.conn.commit()

    def delete_task(self, target_id):
        sql = """
DELETE FROM tasks
WHERE id=?
"""
        self.conn.execute(sql, (target_id,))
        self.conn.commit()

    def load(self):
        with open(self.filename, "r") as d:
            raw_data = json.load(d)
        data = {}
        for key, cls in self.MODEL_MAP.items():
            data[key] = [cls.from_dict(i) for i in raw_data.get(key, [])]
        return data

    def save(self, data: dict):
        j_data = {}
        for key in self.MODEL_MAP.keys():
            j_data[key] = [i.to_dict() for i in data.get(key, [])]
        with open(self.filename, "w") as d:
            json.dump(j_data, d, indent=4)

    def task_add(self, title):
        data = self.load()
        data["tasks"].append(Task(title))
        self.save(data)

    def task_rename(self, target_id, new_title):
        data = self.load()
        self._task_by_id(data, target_id).rename(new_title)
        self.save(data)

    def task_mark(self, target_id):
        data = self.load()
        self._task_by_id(data, target_id).change_status()
        self.save(data)

    def task_delete(self, target_id):
        data = self.load()
        data["tasks"].remove(self._task_by_id(data, target_id))
        self.save(data)

    def log_add(self, content):
        data = self.load()
        data["logs"].append(Log(content))
        self.save(data)

    @staticmethod
    def _task_by_id(data, target_id):
        for task in data["tasks"]:
            if task.id == target_id:
                return task
        raise TaskNotFoundError()
