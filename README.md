# 📝 FastAPI To-Do App

A fully asynchronous To-Do application built with **FastAPI** and **PostgreSQL**. This app provides a robust backend for managing tasks with full CRUD (Create, Read, Update, Delete) functionality. It is designed to be lightweight, fast, and scalable.

---

## 🚀 Features
- Full **CRUD operations** for managing tasks.
- **PostgreSQL** database integration with SQLAlchemy ORM.
- Fully **asynchronous** support for high performance.
- Interactive API documentation with **Swagger UI** and **ReDoc**.
- Pagination support for listing tasks.
- Health check endpoint for monitoring the application.
- Modular and clean code structure for easy scalability.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fastapi-todo-app.git
cd fastapi-todo-app
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL
- Install and configure PostgreSQL on your system.
- Create a new database for the application.
- Update the `.env` file with your database credentials:
  ```env
  DATABASE_URL=postgresql+asyncpg://[your_database_username]:[your_password]@localhost/[your_database_name]
  ```

### 5. Create Database Tables
Run the following script to create the necessary database tables:
```bash
python create_tables.py
```

### 6. Start the Application
Run the FastAPI application using Uvicorn:
```bash
uvicorn app.main:app --reload
```

The application will be available at: [http://localhost:8000](http://localhost:8000)

---

## 📖 API Documentation
FastAPI provides interactive API documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🗂️ Project Structure
```
project1/
├── app/
│   ├── __init__.py          # Package initializer
│   ├── main.py              # Application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas for request/response validation
│   ├── crud.py              # CRUD operations
│   ├── routers/
│   │   ├── __init__.py      # Package initializer for routers
│   │   ├── tasks.py         # Task-related API endpoints
├── create_tables.py         # Script to create database tables
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── README.md                # Project documentation
```

---

## 🧪 Running Tests
To run tests for the application, use the following command:
```bash
pytest
```

---

## 🛡️ Environment Variables
The application uses a `.env` file to manage environment variables. Below are the required variables:
- `DATABASE_URL`: The connection string for the PostgreSQL database.

Example `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/todo_db
```

---

## 🖥️ Example API Endpoints

### 1. Create a Task
**POST** `/tasks/`
```json
{
  "title": "Buy groceries",
  "description": "Milk, Bread, Eggs",
  "completed": false
}
```

### 2. List All Tasks
**GET** `/tasks/`
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, Bread, Eggs",
      "completed": false,
      "created_at": "2025-03-27T12:00:00Z",
      "updated_at": "2025-03-27T12:00:00Z"
    }
  ],
  "count": 1
}
```

### 3. Update a Task
**PUT** `/tasks/{task_id}/`
```json
{
  "title": "Buy groceries and snacks",
  "description": "Milk, Bread, Eggs, Chips",
  "completed": true
}
```

### 4. Delete a Task
**DELETE** `/tasks/{task_id}/`

---

## 🛠️ Technologies Used
- **FastAPI**: Web framework for building APIs.
- **PostgreSQL**: Relational database for storing tasks.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and settings management.
- **Uvicorn**: ASGI server for running the application.

---

## 🙌 Acknowledgments
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)