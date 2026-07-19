import uuid
from datetime import datetime


class Task:
    def __init__(self, title: str, completed=False, id=None, created_at=None):
        self.title = title
        self.id = id if id is not None else str(uuid.uuid4())
        self.completed = completed
        self.created_at = (
            created_at if created_at is not None else datetime.now().isoformat()
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["title"],
            completed=data.get("completed", False),
            id=data.get("id"),
            created_at=data.get("created_at"),
        )

    @classmethod
    def from_sql_row(cls, row):
        return cls(row[1], bool(row[2]), row[0], row[3])

    def change_status(self):
        self.completed = not self.completed

    def rename(self, new_name: str):
        self.title = new_name
