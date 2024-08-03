from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from apps.users import router as user_router
from apps.tasks import router as task_router
app = FastAPI()

# CORS settings
origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()

app.include_router(user_router.router, prefix="/api/v1/users", tags=["users"])
app.include_router(task_router.router, prefix="/api/v1/tasks", tags=["tasks"])