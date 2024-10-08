import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QMessageBox, QLineEdit

# Dictionary to hold tasks
tasks = {}

def load_tasks():
    """Load tasks from a JSON file."""
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            content = file.read()
            if content.strip():  # Check if the file is not empty
                return json.loads(content)
    return {}

def save_tasks():
    """Save tasks to a JSON file."""
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()

        # Task input field
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter a new task or update an existing one...")
        self.layout.addWidget(self.task_input)

        # List widget to display tasks
        self.task_list = QListWidget(self)
        self.layout.addWidget(self.task_list)

        # Buttons for actions
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add/Update Task", self)
        self.add_button.clicked.connect(self.add_or_update_task)
        button_layout.addWidget(self.add_button)

        self.complete_button = QPushButton("Toggle Complete/Incomplete", self)
        self.complete_button.clicked.connect(self.toggle_task_status)
        button_layout.addWidget(self.complete_button)

        self.delete_button = QPushButton("Delete Task", self)
        self.delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        # Load existing tasks on startup
        global tasks
        tasks = load_tasks()  # Load tasks on startup
        self.update_task_list()  # Update the list after loading tasks

    def add_or_update_task(self):
        """Add a new task or update an existing one."""
        description = self.task_input.text().strip()
        if description:
            selected_task = self.task_list.currentRow()
            if selected_task >= 0:  # Update the selected task
                task_ids = list(tasks.keys())
                task_id = task_ids[selected_task]
                tasks[task_id]["description"] = description
                self.task_list.setCurrentRow(-1)  # Deselect task
            else:  # Add a new task
                task_id = len(tasks) + 1
                tasks[task_id] = {"description": description, "completed": False}
            self.task_input.clear()
            save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a task description.")

    def toggle_task_status(self):
        """Mark a task as complete or incomplete."""
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            task_ids = list(tasks.keys())
            task_id = task_ids[selected_task]
            tasks[task_id]["completed"] = not tasks[task_id]["completed"]  # Toggle status
            save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to update its status.")

    def delete_task(self):
        """Delete a task, whether completed or not."""
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            global tasks
            task_ids = list(tasks.keys())
            task_id = task_ids[selected_task]
            del tasks[task_id]
            
            # Reassign new IDs to keep dictionary keys in order
            tasks_reordered = {}
            for i, (tid, details) in enumerate(tasks.items()):
                tasks_reordered[i + 1] = details
            tasks = tasks_reordered

            save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to delete.")

    def update_task_list(self):
        """Update the task list widget to reflect current tasks."""
        self.task_list.clear()
        for task_id, task_details in tasks.items():
            status = "✅" if task_details["completed"] else "❌"
            self.task_list.addItem(f"{task_id}. {task_details['description']} [{status}]")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
