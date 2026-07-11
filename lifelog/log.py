from datetime import datetime


class Log:
    def __init__(self, content, time=None):
        self.content = content
        self.time = (
            time if time is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["content"], data["time"])

    def to_dict(self):
        return {"time": self.time, "content": self.content}
