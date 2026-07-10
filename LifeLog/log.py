from datetime import datetime


class Log:
    def __init__(self, content=""):
        self.time = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        self.content = content

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["content"])

    def to_dict(self):
        return {"time": self.time, "content": self.content}
