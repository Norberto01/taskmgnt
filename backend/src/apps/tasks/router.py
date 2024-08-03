from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schema, service
from database.db import get_db
from functools import lru_cache
from typing import List
from config import settings
import time


router = APIRouter()
CACHE_EXPIRATION_TIME = settings.CACHE_EXPIRE

@lru_cache(maxsize=128)
def cache_get_all_tasks(skip: int, limit: int, db: Session, timestamp: int) -> List[schema.Task]:
    try:
        return service.get_all(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"Error getting tasks: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error getting tasks: {str(e)}")

@router.get("/list", response_model=list[schema.Task])
def get_all_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    current_time = int(time.time() / CACHE_EXPIRATION_TIME) * CACHE_EXPIRATION_TIME
    return cache_get_all_tasks(skip, limit, db, current_time)

@router.post("/create", response_model=schema.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schema.TaskCreate, db: Session = Depends(get_db)):
    try:
        new_task = service.create_task(db=db, task=task)
        cache_get_all_tasks.cache_clear()
        return new_task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Internal server error creating task: {str(e)}")
    
@router.put("/update/{task_id}", response_model=schema.Task)
def update_task(task_id: int, task: schema.TaskUpdate, db: Session = Depends(get_db)):
    try:
        db_task = service.get_by_id(db, task_id)
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        if task.status == schema.TaskStatus.COMPLETED:
            task.completed_at = datetime.now(timezone.utc)
            task.is_completed = True
        updated_task = service.update_task(db, task_id, task)
        cache_get_all_tasks.cache_clear()
        return updated_task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Internal server error updating task: {str(e)}")
    
@router.delete("/delete/{task_id}", response_model=schema.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        db_task = service.get_by_id(db, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        delete_task = service.delete_task(db, task_id=task_id)
        cache_get_all_tasks.cache_clear()
        return delete_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error deleting tasks: {str(e)}")

