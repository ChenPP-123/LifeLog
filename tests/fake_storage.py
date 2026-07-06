class FakeStorage:
    def __init__(self):
        self.task_list = []

    def load(self):
        return self.task_list

    def save(self, data):
        self.task_list = data
