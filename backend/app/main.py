from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import devices, metrics, anomalies, alerts
from app.config.db_init import run_migrations

app = FastAPI(title="NimbusGuard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(anomalies.router, prefix="/anomaly", tags=["anomalies"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])

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
