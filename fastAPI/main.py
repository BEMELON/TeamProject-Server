from typing import Optional
from fastapi import FastAPI
import subprocess
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/detect/bus")
def read_bus():
    subprocess.Popen(['python3', '../scripts/alarmManager.py'])
    return {"body":"1"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
