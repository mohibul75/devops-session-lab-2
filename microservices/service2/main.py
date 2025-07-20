from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import os
import requests

app = FastAPI(title="Service 2")

class Task(BaseModel):
    title: str
    completed: bool = False

tasks = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to Service 2", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/tasks")
def create_task(task: Task):
    task_id = str(len(tasks) + 1)
    tasks[task_id] = task
    return {"task_id": task_id, "task": task}

@app.get("/service1-status")
def get_service1_status():
    try:
        service1_url = os.environ.get("SERVICE1_URL", "http://service1:8000")
        response = requests.get(f"{service1_url}/health")
        return {"service1_status": response.json()}
    except Exception as e:
        return {"service1_status": "unavailable", "error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 