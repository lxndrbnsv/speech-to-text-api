import os
import asyncio

from pydantic import BaseModel
from fastapi import FastAPI

from services.utils import unique_name, download_file
from config import Config as cfg


class TaskState(BaseModel):
    task_id: str


app = FastAPI()


@app.get("/audiofile/{url}")
async def root(url: str):
    filename = f"{unique_name()}.waw"
    task_id = filename.rsplit(".", 1)[0]
    save_path = os.path.join(cfg.AUDIO_FILE_SAVE_PATH, filename)
    asyncio.create_task(download_file(url, save_path))
    return {"task_id": task_id}


@app.post("/task_data")
async def view_data(task: TaskState):
    task_state = "PENDING"
    return dict(state=task_state)
