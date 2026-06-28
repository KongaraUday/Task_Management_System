# Automated Task Management System

A full-stack web application built with Python and Flask 
to automate task creation, tracking and management with 
user authentication and an interactive Bootstrap UI.

## Features

### User Authentication
- User Registration with password hashing
- Secure Login with session management
- Logout functionality

### Dashboard
- Total tasks count
- Pending tasks count
- In Progress tasks count
- Completed tasks count
- High Priority tasks count
- Overall completion rate with progress bar

### Task Management
- Add new tasks with title, description, priority and due date
- View all tasks in a clean responsive table
- Update task status (Pending/In Progress/Completed)
- Delete tasks with confirmation
- Search tasks by title or description
- Color coded priority and status badges

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite
- **Security:** Werkzeug password hashing
- **Version Control:** Git & GitHub
- **IDE:** VS Code

## Project Structure
Task_Management_System/

├── app.py

├── database.py

├── templates/

│   ├── login.html

│   ├── register.html

│   ├── dashboard.html

│   ├── index.html

│   ├── add_task.html

│   └── update_task.html

├── static/

│   └── style.css

└── requirements.txt
## How to Run
1. Clone the repository
   git clone https://github.com/KongaraUday/Task_Management_System.git

2. Install dependencies
   pip install -r requirements.txt

3. Run the application
   python app.py

4. Open browser and go to
   http://127.0.0.1:5000

## Author
Kongara Uday Kiran
B.Tech CSE | SVCET
GitHub: github.com/KongaraUday