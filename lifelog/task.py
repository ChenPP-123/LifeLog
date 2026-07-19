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

    def change_status(self):
        self.completed = not self.completed

    def rename(self, new_name: str):
        self.title = new_name
