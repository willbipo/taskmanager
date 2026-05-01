from task_manager import TaskManager
from ai_service import create_simple_tasks

def print_menu():
    print("\n--- Task Manager ---")
    print("1. Add task")
    print("2. Add complex task")
    print("3. List tasks")
    print("4. Complete task")
    print("5. Remove task")
    print("6. Exit")


def main():

    manager = TaskManager()

    while True:

        print_menu()

        try:
        
            choice = int(input("Choose an option: "))

            match choice:
                case 1:
                    name = input("Task name: ")
                    description = input("Task description: ")
                    manager.add_task(name,description)
                case 2:
                    name = input("Task complex name: ")
                    description = input("Task complex description: ")
                    subtasks = create_simple_tasks(description)
                    for subtask in subtasks:
                        if not subtask.startswith("Error:"):
                            manager.add_task(name,subtask)
                        else:
                            print(subtask)
                            break
                case 3:
                    manager.list_task()
                case 4:
                    task_id = int(input("Task id to complete: "))
                    manager.complete_task(task_id)
                case 5:
                    task_id = int(input("Task id to delete: "))
                    manager.delete_task(task_id)
                case 6:
                    print("Saliendo...")
                    break
                case _:
                    print("Not valid option, choose another option.")

        except ValueError:
            print("Not valid option, choose another option.")
    
if __name__ == "__main__":
    main()