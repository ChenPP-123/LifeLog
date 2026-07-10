class FakeStorage:
    def __init__(self):
        self.data = {"tasks": [], "logs": []}

    def load(self):
        return self.data

    def save(self, data):
        self.data = data
