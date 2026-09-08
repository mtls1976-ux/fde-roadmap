"""Day 8: hello-world FastAPI app.

Run:
    uvicorn app:app --reload
Then open http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI

app = FastAPI(title="fde-roadmap API")


@app.get("/")
def read_root():
    return {"message": "Hello from Day 8 - this is a real backend now."}
