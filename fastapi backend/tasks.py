from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import models
from datetime import datetime
from database import Session

app = FastAPI()
sess = Session()

class Event(BaseModel):
    task_desc: str
    date: datetime

class Event_read(BaseModel):
    task_id: int
    task_desc: str
    date: datetime

class Event_change(BaseModel):
    task_desc: str
    date: datetime


class Gathering(BaseModel):
    id: int
    name: str



@app.get("/")
def login_page():
    return{"message": "Auth later"}

@app.post("/tasks", response_model=Event_read)
def create_task(tasks: Event):
    new_task = models.Task(
        task_desc = tasks.task_desc,
        date = tasks.date
    )
    sess.add(new_task)
    sess.commit()
    return new_task

@app.get("/tasks", response_model=list[Event_read])
def retrieve_tasks():
    tasks = sess.query(models.Task).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks
    


@app.patch("/tasks/{id}")
def update_task(id: int, new_data: Event_change):
    task = sess.query(models.Task).filter(models.Task.task_id == id)    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.update({
        "task_desc": new_data.task_desc     
    })
    sess.commit()
    return {"Message": "Task updated succesfully"}

@app.delete("/tasks/{id}")
def delete_task(id: int):
    task = sess.query(models.Task).filter(models.Task.task_id == id).first()
    """ search_byID = sess.query(models.Task.task_id).all() """
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    sess.delete(task)
    sess.commit()
    return {"message": "Task deleted successfully"}
  
@app.delete("/tasks")
def delete_tasks():
    sess.query(models.Task).delete()
    sess.commit()
    return {"message": "All tasks deleted successfully"}

    

    

    



