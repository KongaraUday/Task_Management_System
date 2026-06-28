from database import create_connection

def add_task(title, description, priority, due_date):
    """Add a new task to the database"""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO tasks (title, description, priority, due_date, status)
        VALUES (?, ?, ?, ?, 'Pending')
    """, (title, description, priority, due_date))
    
    conn.commit()
    conn.close()
    print(f"\n✅ Task '{title}' added successfully!")

def view_tasks():
    """View all tasks from database"""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        print("\n⚠️ No tasks found!")
        return
    
    print("\n📋 ALL TASKS:")
    print("-" * 60)
    for task in tasks:
        print(f"ID       : {task[0]}")
        print(f"Title    : {task[1]}")
        print(f"Details  : {task[2]}")
        print(f"Priority : {task[3]}")
        print(f"Due Date : {task[4]}")
        print(f"Status   : {task[5]}")
        print("-" * 60)

def update_task(task_id, status):
    """Update task status"""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE tasks SET status = ? WHERE id = ?
    """, (status, task_id))
    
    conn.commit()
    conn.close()
    print(f"\n✅ Task {task_id} updated to '{status}' successfully!")

def delete_task(task_id):
    """Delete a task from database"""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    conn.commit()
    conn.close()
    print(f"\n✅ Task {task_id} deleted successfully!")

def search_task(keyword):
    """Search tasks by keyword"""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM tasks 
        WHERE title LIKE ? OR description LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        print(f"\n⚠️ No tasks found with keyword '{keyword}'!")
        return
    
    print(f"\n🔍 SEARCH RESULTS FOR '{keyword}':")
    print("-" * 60)
    for task in tasks:
        print(f"ID       : {task[0]}")
        print(f"Title    : {task[1]}")
        print(f"Priority : {task[3]}")
        print(f"Status   : {task[5]}")
        print("-" * 60)