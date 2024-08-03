from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db_base import Base
from apps.tasks.model import Task

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)
    address = Column(String)
    
    tasks = relationship("Task", back_populates="user")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}