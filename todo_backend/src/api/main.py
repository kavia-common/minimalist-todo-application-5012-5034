from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List

from .db import get_connection, initialize_db
from .schemas import Task, TaskIn

app = FastAPI(
    title="Minimalist TODO API",
    description="Minimalistic API to manage Todo tasks.",
    version="1.0.0",
    openapi_tags=[
        {"name": "tasks", "description": "Operations related to Todo tasks"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def setup_db():
    initialize_db()

@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint to verify API is running"""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/tasks", response_model=List[Task], tags=["tasks"], summary="Get all tasks", description="Retrieve the list of all todo tasks.", responses={200: {"description": "List of tasks"}})
def list_tasks():
    """
    Fetch all todo tasks.
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, completed FROM tasks")
        tasks_rows = c.fetchall()
        return [
            Task(id=row[0], title=row[1], completed=bool(row[2]))
            for row in tasks_rows
        ]

# PUBLIC_INTERFACE
@app.post("/tasks", response_model=Task, status_code=201, tags=["tasks"], summary="Create a task", description="Create a new todo task.", responses={201: {"description": "Task created"}})
def add_task(task: TaskIn):
    """
    Create a new todo task.
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            (task.title, int(task.completed))
        )
        conn.commit()
        new_id = c.lastrowid
        return Task(id=new_id, **task.dict())

# PUBLIC_INTERFACE
@app.put("/tasks/{task_id}", response_model=Task, tags=["tasks"], summary="Update a task", description="Update an existing todo task.", responses={404: {"description": "Task not found"}})
def update_task(task_id: int, task: TaskIn):
    """
    Update an existing todo task by ID.
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if not c.fetchone():
            raise HTTPException(status_code=404, detail="Task not found")
        c.execute(
            "UPDATE tasks SET title=?, completed=? WHERE id=?",
            (task.title, int(task.completed), task_id)
        )
        conn.commit()
        return Task(id=task_id, **task.dict())

# PUBLIC_INTERFACE
@app.delete("/tasks/{task_id}", response_model=dict, tags=["tasks"], summary="Delete a task", description="Delete a todo task by ID.", responses={404: {"description": "Task not found"}})
def delete_task(task_id: int):
    """
    Delete an existing todo task by ID.
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM tasks WHERE id=?", (task_id,))
        if not c.fetchone():
            raise HTTPException(status_code=404, detail="Task not found")
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        return {"message": "Task deleted"}
