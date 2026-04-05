from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.user import router as user_router
from app.database import engine, Base
from app.models import User, Note
from app.routes.note import router as note_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(user_router)
app.include_router(note_router)

@app.get("/")
def root():
    return {"message": "Backend is alive"}