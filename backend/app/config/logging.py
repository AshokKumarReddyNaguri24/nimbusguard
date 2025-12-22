import logging
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config.settings import settings

_request_id: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id.get()
        return True


def set_request_id(request_id: str):
    return _request_id.set(request_id)


def reset_request_id(token) -> None:
    _request_id.reset(token)


def setup_logging():
    """
    Logs to:
      - backend/logs/app.log (rotating)
      - stdout (console)
    """
    # backend/app/config/logging.py -> parents[2] = backend/
    backend_dir = Path(__file__).resolve().parents[2]
    logs_dir = backend_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "app.log"

    root_logger = logging.getLogger()
    level_name = settings.LOG_LEVEL.upper()
    level = getattr(logging, level_name, logging.INFO)
    root_logger.setLevel(level)

    # Prevent duplicate handlers if reload/import happens
    if root_logger.handlers:
        return

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(request_id)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(level)
    file_handler.addFilter(RequestIdFilter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)
    console_handler.setLevel(level)
    console_handler.addFilter(RequestIdFilter())

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
