import json
import os

from .log import Log
from .task import Task


class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.MODEL_MAP = {"tasks": Task, "logs": Log}

        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            with open(self.filename, "w") as d:
                json.dump({"tasks": [], "logs": []}, d, indent=4)

    def load(self):
        with open(self.filename, "r") as d:
            raw_data = json.load(d)
        data = {}
        for key, cls in self.MODEL_MAP.items():
            data[key] = [cls.from_dict(i) for i in raw_data.get(key, [])]
        return data

    def save(self, data: dict):
        j_data = {}
        for key in self.MODEL_MAP.keys():
            j_data[key] = [i.to_dict() for i in data.get(key, [])]
        with open(self.filename, "w") as d:
            json.dump(j_data, d, indent=4)

    def task_add(self,title):
        data=self.load()
        data["tasks"].append(Task(title))
        self.save(data)

    def task_rename(self,target_id,new_title):
        data=self.load()
        target=next((task for task in data["tasks"] if task.id ==target_id),None)
        if target:
            target.rename(new_title)
        self.save(data)
    
    def task_mark(self,target_id):
        data=self.load()
        target=next((task for task in data["tasks"] if task.id ==target_id),None)
        if target:
            target.change_status()
        self.save(data)
    
    def task_delete(self,target_id):
        data=self.load()
        target=next((task for task in data["tasks"] if task.id ==target_id),None)
        if target:
            data["tasks"].remove(target)
        self.save(data)