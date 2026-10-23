from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine, settings
from app.middleware import RequestMetricsMiddleware, get_metrics
from app.routes.tasks import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan,
              description="Async CRUD API for learning backend fundamentals.")
app.add_middleware(RequestMetricsMiddleware)
app.include_router(tasks_router)

@app.get("/", tags=["system"])
async def root():
    return {"message": "API is running", "docs": "/docs"}

@app.get("/health", tags=["system"])
async def health():
    return {"status": "healthy"}

@app.get("/metrics", tags=["system"])
async def metrics():
    return get_metrics()
