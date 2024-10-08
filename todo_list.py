# todo_list.py

# A dictionary to hold tasks, using task number as the key
tasks = {}

def show_menu():
    print("\n==== To-Do List Menu ====")
    print("1. View To-Do List")
    print("2. Add a New Task")
    print("3. Mark Task as Complete")
    print("4. Delete a Task")
    print("5. Exit")

def view_tasks():
    print("\n==== Current To-Do List ====")
    if not tasks:
        print("Your to-do list is empty.")
    else:
        for task_id, task_details in tasks.items():
            status = "Done" if task_details['completed'] else "Pending"
            print(f"{task_id}. {task_details['description']} - [{status}]")

def add_task():
    description = input("Enter the task description: ")
    task_id = len(tasks) + 1
    tasks[task_id] = {"description": description, "completed": False}
    print(f"Task '{description}' added successfully.")

def mark_task_complete():
    task_id = int(input("Enter the task number to mark as complete: "))
    if task_id in tasks:
        tasks[task_id]['completed'] = True
        print(f"Task {task_id} marked as complete.")
    else:
        print(f"No task found with ID {task_id}.")

def delete_task():
    task_id = int(input("Enter the task number to delete: "))
    if task_id in tasks:
        deleted_task = tasks.pop(task_id)
        print(f"Task '{deleted_task['description']}' deleted.")
    else:
        print(f"No task found with ID {task_id}.")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ")
        if choice == '1':
            view_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            mark_task_complete()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("Exiting the program. Have a great day!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
