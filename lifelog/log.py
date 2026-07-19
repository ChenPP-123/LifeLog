import uuid
from datetime import datetime


class Log:
    def __init__(self, content, created_at=None, id=None):
        self.content = content
        self.id = id if id is not None else str(uuid.uuid4())
        self.created_at = (
            created_at if created_at is not None else datetime.now().isoformat()
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["content"], time=data.get("time"), id=data.get("id"))

    @classmethod
    def from_sql_row(cls, row):
        return cls(row[1], row[2], row[0])

    def to_dict(self):
        return {"id": self.id, "time": self.time, "content": self.content}
