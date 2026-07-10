class Task:
    def __init__(self, title: str, completed=False):
        self.title = title
        self.completed = completed

    def to_dict(self):
        return {"title": self.title, "completed": self.completed}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["title"], data["completed"])

    def change_status(self):
        self.completed = not self.completed

    def rename(self, new_name: str):
        self.title = new_name
