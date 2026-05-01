from task_manager import TaskManager

def print_menu():
    print("\n--- Task Manager ---")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete task")
    print("4. Remove task")
    print("5. Exit")


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
                    manager.list_task()
                case 3:
                    task_id = int(input("Task id to complete: "))
                    manager.complete_task(task_id)
                case 4:
                    task_id = int(input("Task id to delete: "))
                    manager.delete_task(task_id)
                case 5:
                    print("Saliendo...")
                    break
                case _:
                    print("Not valid option, choose another option.")

        except ValueError:
            print("Not valid option, choose another option.")
    
if __name__ == "__main__":
    main()