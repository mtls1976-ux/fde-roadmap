"""Day 8-9: FastAPI app - hello world, path params, and a POST body.

Run:
    uvicorn app:app --reload
Then open http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
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


@app.post("/tasks")
def create_task(task: TaskIn):
    """POST body example - Pydantic validates the JSON before this even runs.

    Not saved anywhere yet (real storage arrives Day 11) - this just proves
    the request body is being received and parsed correctly.
    """
    return {"received": task, "note": "not saved yet - Day 11 adds real storage"}
