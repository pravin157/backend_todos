# Todo Backend (Django + PostgreSQL)

## Setup Instructions

1. **Create Database in pgAdmin**:
   - Open **pgAdmin 4**.
   - Expand your PostgreSQL Server.
   - Right-click **Databases** -> **Create** -> **Database...**
   - Database name: 	odo_db
   - Click **Save**.

2. **Configure .env**:
   - Open .env in ackend folder.
   - Update DB_PASSWORD with your PostgreSQL password:
     `env
     DB_NAME=todo_db
     DB_USER=postgres
     DB_PASSWORD=your_actual_postgres_password
     DB_HOST=localhost
     DB_PORT=5432
     `

3. **Run Migrations**:
   `powershell
   cd D:\test_application\backend
   .\venv\Scripts\activate
   python manage.py migrate
   `

4. **Start Development Server**:
   `powershell
   python manage.py runserver
   `
   API URL: http://127.0.0.1:8000/api/todos/
