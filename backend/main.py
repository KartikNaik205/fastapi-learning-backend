from fastapi import FastAPI
from app.routes.health import router as health_router
from app.schemas.health import HealthResponse

app = FastAPI()

app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Backend is alive"}