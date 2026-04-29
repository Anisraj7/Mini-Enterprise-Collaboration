from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routers import activity, approval, auth, comments, dashboard, kanban, tasks, users

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(kanban.router)
app.include_router(comments.router)
app.include_router(approval.router)
app.include_router(dashboard.router)
app.include_router(activity.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
