import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.users import service, schema
from database.db import get_db
from functools import lru_cache
from typing import List
from config import settings
import time

router = APIRouter()
CACHE_EXPIRATION_TIME = settings.CACHE_EXPIRE

@lru_cache(maxsize=128)
def cache_get_all_users(skip: int, limit: int, db: Session, timestamp: int) -> List[schema.User]:
    try:
        return service.get_all(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error getting users: {str(e)}")

@router.get("/list", response_model=list[schema.User], status_code=status.HTTP_200_OK)
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    current_time = int(time.time() / CACHE_EXPIRATION_TIME) * CACHE_EXPIRATION_TIME
    return cache_get_all_users(skip, limit, db, current_time)

@router.post("/create", response_model=schema.User, status_code=status.HTTP_201_CREATED)
def create_user(user_data_set: schema.UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Received create user request: {user_data_set}")
        db_user = service.get_by_email(db, email=user_data_set.email)
        if db_user:
            raise HTTPException(status_code=400, detail="User already registered")
        new_user = service.create_usr(db=db, user=user_data_set)
        cache_get_all_users.cache_clear()
        return new_user
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error creating user: {str(e)} - {time.ctime()}")

@router.delete("/delete/{user_id}", response_model=schema.User, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = service.get_by_id(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        delete_user = service.delete_usr(db=db, user_id=user_id)
        cache_get_all_users.cache_clear()
        return delete_user
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error deleting user: {str(e)}")
