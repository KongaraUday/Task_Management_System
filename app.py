from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import create_connection, create_table
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "taskmanager2026"

# Create tables on startup
create_table()

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (?, ?)
            """, (username, hashed_password))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except:
            flash("Username already exists! Try another.", "danger")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

# ============================================
# DASHBOARD ROUTE
# ============================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = create_connection()
    cursor = conn.cursor()
    user_id = session["user_id"]

    # Task Statistics
    cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE user_id=?", (user_id,))
    total = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE user_id=? AND status='Pending'", (user_id,))
    pending = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE user_id=? AND status='In Progress'", (user_id,))
    in_progress = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE user_id=? AND status='Completed'", (user_id,))
    completed = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE user_id=? AND priority='High'", (user_id,))
    high_priority = cursor.fetchone()["count"]

    conn.close()

    # Calculate completion percentage
    percentage = round((completed / total * 100), 1) if total > 0 else 0

    return render_template("dashboard.html",
        total=total,
        pending=pending,
        in_progress=in_progress,
        completed=completed,
        high_priority=high_priority,
        percentage=percentage
    )

# ============================================
# TASK ROUTES
# ============================================

@app.route("/tasks")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    keyword = request.args.get("keyword", "")
    conn = create_connection()
    cursor = conn.cursor()
    user_id = session["user_id"]

    if keyword:
        cursor.execute("""
            SELECT * FROM tasks
            WHERE user_id=? AND (title LIKE ? OR description LIKE ?)
        """, (user_id, f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))

    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks, keyword=keyword)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]
        user_id = session["user_id"]

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
        """, (user_id, title, description, priority, due_date))
        conn.commit()
        conn.close()
        flash("Task added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add_task.html")

@app.route("/update/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = create_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        status = request.form["status"]
        cursor.execute("UPDATE tasks SET status=? WHERE id=?",
                      (status, task_id))
        conn.commit()
        conn.close()
        flash("Task updated successfully!", "success")
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return render_template("update_task.html", task=task)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    flash("Task deleted successfully!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)