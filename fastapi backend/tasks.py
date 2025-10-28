from fastapi import FastAPI, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import models
from datetime import datetime
from database import Session
from sqlalchemy import text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)
sess = Session()

class Event(BaseModel):
    task_desc: str
    date: Optional[datetime] = None

class Event_read(BaseModel):
    task_id: int
    task_desc: str
    date: datetime

class Event_change(BaseModel):
    task_desc: str


class Gathering(BaseModel):
    id: int
    name: str



@app.get("/")
def login_page():
    return{"message": "Auth later"}

@app.post("/tasks", response_model=Event_read, status_code=201)
def create_task(tasks: Event):
    new_task = models.Task(
        task_desc = tasks.task_desc,
        date = tasks.date if tasks.date else datetime.now()
    )
    sess.add(new_task)
    sess.commit()
    return new_task

@app.get("/tasks", response_model=list[Event_read], status_code=200)
def retrieve_tasks():
    tasks = sess.query(models.Task).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks
    


@app.patch("/tasks/{id}")
def update_task(id: int, new_data: Event_change):
    task_query = sess.query(models.Task).filter(models.Task.task_id == id)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_query.update({"task_desc": new_data.task_desc})
    sess.commit()
    return {"message": "Task updated successfully"}

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    task = sess.query(models.Task).filter(models.Task.task_id == id).first() 
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    sess.delete(task)
    sess.commit()
    return {"message": "Task deleted successfully"}
  
@app.delete("/tasks", status_code=204)
def reset_tasks():
    sess.query(models.Task).delete()
    sess.execute(text("ALTER SEQUENCE tasks_id_seq RESTART WITH 1;"))
    sess.commit()
    return {"message": "All tasks deleted successfully"}

    

    

    



