from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="Todo API",
    description="Uma API simples para gerenciar tarefas",
    version="1.0.0"
)

# Constantes
TASK_NOT_FOUND_MSG = "Tarefa não encontrada"

# Modelo de dados para uma tarefa
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Armazenamento em memória (para simplicidade)
tasks_db = {}

@app.get("/")
async def root():
    return {"message": "Todo API - Sistema de Gerenciamento de Tarefas"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    task_id = str(uuid.uuid4())
    now = datetime.now()
    
    new_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=False,
        created_at=now,
        updated_at=now
    )
    
    tasks_db[task_id] = new_task
    return new_task

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return list(tasks_db.values())

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=TASK_NOT_FOUND_MSG)
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=TASK_NOT_FOUND_MSG)
    
    stored_task = tasks_db[task_id]
    update_data = task_update.dict(exclude_unset=True)
    
    # Atualiza apenas os campos fornecidos
    for field, value in update_data.items():
        setattr(stored_task, field, value)
    
    stored_task.updated_at = datetime.now()
    tasks_db[task_id] = stored_task
    
    return stored_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=TASK_NOT_FOUND_MSG)
    
    deleted_task = tasks_db.pop(task_id)
    return {"message": f"Tarefa '{deleted_task.title}' deletada com sucesso"}

@app.get("/tasks/status/{completed}")
async def get_tasks_by_status(completed: bool):
    filtered_tasks = [task for task in tasks_db.values() if task.completed == completed]
    return filtered_tasks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
