from fastapi import FastAPI
import datetime

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Empire of 8 — COA online",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/route")
def route_task(task: str):
    # Placeholder routing logic
    return {"status": "received", "task": task, "agent": "Finance (mock)"}
