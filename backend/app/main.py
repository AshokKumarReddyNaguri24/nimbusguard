import time
import uuid
from fastapi import FastAPI, Request
from app.api import devices, metrics, anomalies, health
from app.config.db_init import run_migrations, validate_environment
from app.config.logging import setup_logging, get_logger, set_request_id, reset_request_id
from app.services.scheduler import start_scheduler, shutdown_scheduler

setup_logging()
logger = get_logger(__name__)

app = FastAPI(title="NimbusGuard API")

app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(anomalies.router, prefix="/anomalies", tags=["anomalies"])
app.include_router(health.router, prefix="/health", tags=["health"])


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = set_request_id(request_id)
    start = time.time()
    try:
        response = await call_next(request)
    except Exception:
        logger.error("API %s %s failed", request.method, request.url.path, exc_info=True)
        raise
    else:
        ms = int((time.time() - start) * 1000)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "API %s %s -> %s (%sms)",
            request.method,
            request.url.path,
            response.status_code,
            ms,
        )
        return response
    finally:
        reset_request_id(token)


@app.on_event("startup")
async def startup_event():
    logger.info("Backend startup initiated")

    validate_environment()
    run_migrations()

    start_scheduler()

    logger.info("Backend startup completed successfully")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Backend shutdown initiated")
    shutdown_scheduler()
    logger.info("Backend shutdown completed")

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
