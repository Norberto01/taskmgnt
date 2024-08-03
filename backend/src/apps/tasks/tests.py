# tests/tasks/test_service.py
from datetime import datetime, timedelta, timezone
from apps.tasks.service import create_task, get_by_id, get_all, delete_task, update_task
from apps.tasks.model import TaskStatus, TaskPriority
from apps.tasks.schema import TaskCreate, TaskUpdate
from tests.connect import db

def test_create_task(db):
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id=1,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    db_task = create_task(db, task_data)
    assert db_task.id is not None
    assert db_task.title == "Test Task"
    assert db_task.description == "This is a test task"
    assert db_task.user_id == 1
    assert db_task.status == TaskStatus.PENDING
    assert db_task.priority == TaskPriority.MEDIUM


def test_get_by_id(db):
    task_data = TaskCreate(
        title="Task by ID",
        description="Testing get by ID",
        user_id=1,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    db_task = create_task(db, task_data)
    fetched_task = get_by_id(db, db_task.id)
    assert fetched_task.id == db_task.id

def test_get_all(db):
    task_data_1 = TaskCreate(
        title="Task One",
        description="First task",
        user_id=1,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    task_data_2 = TaskCreate(
        title="Task Two",
        description="Second task",
        user_id=1,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    create_task(db, task_data_1)
    create_task(db, task_data_2)
    tasks = get_all(db)
    assert len(tasks) >= 2

def test_delete_task(db):
    task_data = TaskCreate(
        title="Task to Delete",
        description="Task that will be deleted",
        user_id=1,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    db_task = create_task(db, task_data)
    deleted_task = delete_task(db, db_task.id)
    assert deleted_task is not None
    assert get_by_id(db, db_task.id) is None

def test_update_task(db):
    task_data = TaskCreate(
        title="Task to Update",
        description="Task that will be updated",
        user_id=1,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    db_task = create_task(db, task_data)
    task_dataset = TaskUpdate(
        user_id=1,
        title="Updated Task Title",
        description="Updated task description"
    )
    updated_task = update_task(db, db_task.id, task_dataset)
    assert updated_task.title == task_dataset.title
    assert updated_task.description == task_dataset.description
