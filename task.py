class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def to_dict(self):
        return {"title": self.title, "completed": self.completed}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["completed"])

    def change_status(self):
        self.completed = not self.completed
