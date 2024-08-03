from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .model import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    user_id: Optional[int]
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskCreate(TaskBase):
    title: str
    description: str
    user_id: int
    due_date: datetime
    status: TaskStatus
    priority: TaskPriority
    is_completed: Optional[bool] = False

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: int
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class TaskInDBBase(TaskBase):
    id: Optional[int]
    creation_date: datetime
    is_completed: bool

    model_config = {
        "from_attributes": True
    }

class Task(TaskInDBBase):
    pass
