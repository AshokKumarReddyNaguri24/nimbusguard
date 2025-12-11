from fastapi import FastAPI
from app.api import devices, metrics
from app.config.db_init import run_migrations

app = FastAPI(title="NimbusGuard API")

app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

@app.on_event("startup")
async def startup_event():
    run_migrations()
    from app.services import scheduler
    scheduler.start_scheduler()

@app.get("/")
async def root():
    return {"message": "I am alive"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
