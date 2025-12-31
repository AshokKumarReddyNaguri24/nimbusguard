from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.config import database
from app.config.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


def _check_engine(engine, label: str) -> dict:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        logger.error("Health check failed: %s", label, exc_info=True)
        return {"status": "error"}


@router.get("/")
def health_check(response: Response):
    inventory = _check_engine(database.engine_inventory, "inventory_db")
    metrics = _check_engine(database.engine_metrics, "metrics_db")
    overall = "ok" if inventory["status"] == "ok" and metrics["status"] == "ok" else "degraded"
    response.status_code = status.HTTP_200_OK if overall == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "status": overall,
        "inventory_db": inventory,
        "metrics_db": metrics,
    }
