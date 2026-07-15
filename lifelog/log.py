import uuid
from datetime import datetime


class Log:
    def __init__(self, content, time=None, id=None):
        self.content = content
        self.id = id if id is not None else str(uuid.uuid4())
        self.time = (
            time if time is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["content"], time=data.get("time"), id=data.get("id"))

    def to_dict(self):
        return {"id": self.id, "time": self.time, "content": self.content}
