from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.user import router as user_router
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Backend is alive"}
