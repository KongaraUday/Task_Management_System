from database import create_table
from tasks import add_task, view_tasks, update_task, delete_task, search_task

def main_menu():
    """Display main menu and handle user input"""
    create_table()
    
    while True:
        print("\n" + "=" * 40)
        print("   AUTOMATED TASK MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. ➕ Add New Task")
        print("2. 📋 View All Tasks")
        print("3. ✏️  Update Task Status")
        print("4. 🗑️  Delete Task")
        print("5. 🔍 Search Task")
        print("6. 🚪 Exit")
        print("=" * 40)
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            print("\n--- ADD NEW TASK ---")
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            print("Priority options: High / Medium / Low")
            priority = input("Enter priority: ")
            due_date = input("Enter due date (DD-MM-YYYY): ")
            add_task(title, description, priority, due_date)
            
        elif choice == "2":
            view_tasks()
            
        elif choice == "3":
            print("\n--- UPDATE TASK STATUS ---")
            view_tasks()
            task_id = int(input("\nEnter Task ID to update: "))
            print("Status options: Pending / In Progress / Completed")
            status = input("Enter new status: ")
            update_task(task_id, status)
            
        elif choice == "4":
            print("\n--- DELETE TASK ---")
            view_tasks()
            task_id = int(input("\nEnter Task ID to delete: "))
            confirm = input(f"Are you sure you want to delete Task {task_id}? (yes/no): ")
            if confirm.lower() == "yes":
                delete_task(task_id)
            else:
                print("❌ Deletion cancelled!")
                
        elif choice == "5":
            print("\n--- SEARCH TASK ---")
            keyword = input("Enter keyword to search: ")
            search_task(keyword)
            
        elif choice == "6":
            print("\n👋 Thank you for using Task Management System!")
            print("Goodbye Uday! 🚀")
            break
            
        else:
            print("\n⚠️ Invalid choice! Please enter 1-6.")

if __name__ == "__main__":
    main_menu()