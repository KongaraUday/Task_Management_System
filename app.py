from flask import Flask, render_template, request, redirect, url_for
from database import create_connection, create_table

app = Flask(__name__)

# Create table on startup
create_table()

@app.route("/")
def index():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, due_date, status)
            VALUES (?, ?, ?, ?, 'Pending')
        """, (title, description, priority, due_date))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_task.html")

@app.route("/update/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        status = request.form["status"]
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?",
                      (status, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return render_template("update_task.html", task=task)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))
@app.route("/search")
def search_task():
    keyword = request.args.get("keyword", "")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tasks 
        WHERE title LIKE ? OR description LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)