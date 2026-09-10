"""Day 8-11: FastAPI app - routes, validation, and a full in-memory CRUD API.

Run:
    uvicorn app:app --reload
Then open http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI(title="fde-roadmap API")


@app.get("/")
def read_root():
    return {"message": "Hello from Day 8 - this is a real backend now."}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Path parameter example - FastAPI parses user_id as an int for us."""
    return {"user_id": user_id, "name": f"User {user_id}"}


class TaskIn(BaseModel):
    title: str              # required - no default means the client MUST send it
    done: bool = False      # optional - has a default, so the client may omit it
    priority: str = "normal"  # optional, but constrained by the custom validator below

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        """Type-checking alone lets "   " through since it's a valid str -
        this catches the case type validation misses."""
        if not v.strip():
            raise ValueError("title cannot be blank")
        return v.strip()

    @field_validator("priority")
    @classmethod
    def priority_must_be_known(cls, v):
        allowed = {"low", "normal", "high"}
        if v not in allowed:
            raise ValueError(f"priority must be one of {sorted(allowed)}, got {v!r}")
        return v


class Task(TaskIn):
    id: int


# In-memory "database" - just a dict keyed by id. Gone on every restart;
# Day 39 replaces this with real Postgres storage.
tasks_db: dict[int, Task] = {}
next_id = 1


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskIn):
    global next_id
    new_task = Task(id=next_id, **task.model_dump())
    tasks_db[next_id] = new_task
    next_id += 1
    return new_task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskIn):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    updated = Task(id=task_id, **task.model_dump())
    tasks_db[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    del tasks_db[task_id]
