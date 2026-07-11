from copy import deepcopy


class FakeStorage:
    def __init__(self, data=None):
        self.data = deepcopy(data) if data is not None else {"tasks": [], "logs": []}
        self.load_calls = 0
        self.save_calls = 0
        self.saved_snapshots = []

    def load(self):
        self.load_calls += 1
        return self.data

    def save(self, data):
        self.save_calls += 1
        self.saved_snapshots.append(deepcopy(data))
        self.data = data
