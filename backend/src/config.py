import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Tskm Project"
    SQLALCHEMY_DATABASE_URI: str = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_SERVER")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    CACHE_EXPIRE: int = 3600

settings = Settings()
