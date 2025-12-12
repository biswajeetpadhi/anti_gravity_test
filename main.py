import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import engine, Base, get_db
from models import Task

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# --- Pydantic Models ---
class TaskSchema(BaseModel):
    id: int
    content: str
    
    class Config:
        orm_mode = True

class TaskInput(BaseModel):
    task: str

# --- API Endpoints ---
@app.get("/api/tasks", response_model=dict)
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    # Transform to list of dicts for JSON
    return {"tasks": [{"id": t.id, "content": t.content} for t in tasks]}

@app.post("/api/tasks")
async def add_task(task_input: TaskInput, db: AsyncSession = Depends(get_db)):
    new_task = Task(content=task_input.task)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    
    # Return updated list
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return {"tasks": [{"id": t.id, "content": t.content} for t in tasks]}

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if task:
        await db.delete(task)
        await db.commit()
        
        # Return updated list
        result = await db.execute(select(Task))
        tasks = result.scalars().all()
        return {"tasks": [{"id": t.id, "content": t.content} for t in tasks]}
    
    raise HTTPException(status_code=404, detail="Task not found")

# --- Frontend ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
