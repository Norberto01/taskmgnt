from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .model import User
from .schema import UserCreate
from typing import Optional
import logging


logger = logging.getLogger(__name__)

def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_usr(db: Session, user: UserCreate) -> User:
    try:
        db_user = User(**user.model_dump(exclude_unset=True))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        return None

def delete_usr(db: Session, user_id: int) -> Optional[User]:
    try:
        result = db.query(User).filter(User.id == user_id).first()
        if result:
            db.delete(result)
            db.commit()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error deleting user: {str(e)}")
        db.rollback()
        return None