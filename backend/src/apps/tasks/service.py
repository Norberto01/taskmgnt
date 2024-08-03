from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .model import Task, TaskStatus
from .schema import TaskCreate, TaskUpdate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def get_by_id(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    return db.query(Task).filter(
        Task.status != TaskStatus.COMPLETED,
        Task.status != TaskStatus.CANCELLED,
        Task.is_completed == False
        ).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate) -> Task:
    try:
        db_task = Task(**task.model_dump(exclude_unset=True))
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Error creating task: {str(e)}")
        db.rollback()
        return None

def delete_task(db: Session, task_id: int) -> Optional[Task]:
    try:
        result = db.query(Task).filter(Task.id == task_id).first()
        if result:
            db.delete(result)
            db.commit()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error deleting task: {str(e)}")
        db.rollback()
        return None

def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[Task]:
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
        
        update_data = task.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_task, key, value)

        if task.status == TaskStatus.COMPLETED:
            db_task.is_completed = True
            db_task.completed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Error updating task: {str(e)}")
        db.rollback()
        return None