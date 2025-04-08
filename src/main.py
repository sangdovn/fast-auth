from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.database import init_db

# Create tables before app starts
init_db()

app = FastAPI()
app.include_router(auth_router)
