"""Day 8-9: FastAPI app - hello world, path params, and a POST body.

Run:
    uvicorn app:app --reload
Then open http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="fde-roadmap API")


@app.get("/")
def read_root():
    return {"message": "Hello from Day 8 - this is a real backend now."}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Path parameter example - FastAPI parses user_id as an int for us."""
    return {"user_id": user_id, "name": f"User {user_id}"}


class TaskIn(BaseModel):
    title: str
    done: bool = False


@app.post("/tasks")
def create_task(task: TaskIn):
    """POST body example - Pydantic validates the JSON before this even runs.

    Not saved anywhere yet (real storage arrives Day 11) - this just proves
    the request body is being received and parsed correctly.
    """
    return {"received": task, "note": "not saved yet - Day 11 adds real storage"}
