"""
PlantGuard AI – Main FastAPI application entry point
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.database import init_db
from app.routes import analyze, history, analytics, library, treatment


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="PlantGuard AI",
    description="AI-based Plant Disease Detection & Treatment Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(library.router, prefix="/api/library", tags=["Library"])
app.include_router(treatment.router, prefix="/api/treatment", tags=["Treatment"])


@app.get("/")
async def root():
    return {"message": "PlantGuard AI API is running", "version": "1.0.0"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
