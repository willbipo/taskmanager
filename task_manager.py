import json

class Task:

    def __init__(self, id, name, description, completed = False ):
        self.id = id
        self.name = name
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✓" if self.completed else " "
        return f"[{status}] #{self.id}: {self.name}"
    
class TaskManager:

    FILENAME = "tasks.json"

    def __init__(self):
        self._tasks = []
        self._next_id = 1
        self.load_tasks()

    def add_task(self, name, description):
        task = Task(self._next_id, name, description)
        self._tasks.append(task)
        self._next_id += 1
        self.save_tasks()
        print(f"Task added: {task.name}")

    def list_task(self):
        if len(self._tasks)>0:
            for task in self._tasks:
                print(task)
        else:
            print("Tasks not found")

    def complete_task(self, id):
        for task in self._tasks:
            if task.id == id:
                task.completed = True
                self.save_tasks()
                print(f"Task completed: {task.name}")
                return
        print(f"Task not found: {id}")

    def delete_task(self, id):
        for task in self._tasks:
            if task.id == id:
                self._tasks.remove(task)
                self.save_tasks()
                print(f"Task removed: {id}")
                return
        print(f"Task not found: {id}")

    def load_tasks(self):
        try:
            with open(self.FILENAME, "r") as file:
                data = json.load(file)
                self._tasks = [Task(item["id"], item["name"], item["description"], item["completed"]) for item in data]
                if self._tasks:
                    self._next_id = self._tasks[-1].id + 1
                else:
                    self._next_id = 1
        except FileNotFoundError:
            self._tasks = []


    def save_tasks(self):
        with open(self.FILENAME, "w") as file:
            json.dump([{"id": task.id, "name": task.name, "description": task.description, "completed": task.completed} for task in self._tasks], file, indent = 4)
