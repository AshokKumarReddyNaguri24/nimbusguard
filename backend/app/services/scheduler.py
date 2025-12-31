from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_RUNNING
from app.config.database import SessionLocal
from app.models import device as device_models
from app.services import snmp_collector
from app.config.logging import get_logger

logger = get_logger(__name__)

_scheduler = AsyncIOScheduler()
_JOB_ID = "poll_all_devices"


def poll_all_devices():
    logger.info("Scheduler job started: poll_all_devices")
    db = SessionLocal()
    try:
        devices = db.query(device_models.Device).all()
        logger.info("Scheduler run: devices_to_poll=%s", len(devices))

        for device in devices:
            try:
                snmp_collector.collect_metrics(device)
            except Exception:
                logger.error(
                    "Error polling device name=%s ip=%s",
                    device.name,
                    device.ip_address,
                    exc_info=True,
                )

    except Exception:
        logger.error("Scheduler job failed: poll_all_devices", exc_info=True)
    finally:
        db.close()
        logger.info("Scheduler job finished: poll_all_devices")


def start_scheduler():
    if _scheduler.state == STATE_RUNNING:
        logger.info("Scheduler already running; skipping start")
        return

    _scheduler.add_job(
        poll_all_devices,
        "interval",
        minutes=1,
        id=_JOB_ID,
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=30,
    )
    _scheduler.start()
    logger.info("Scheduler started successfully (job_id=%s, interval=1min)", _JOB_ID)


def shutdown_scheduler():
    try:
        if _scheduler.state == STATE_RUNNING:
            _scheduler.shutdown(wait=False)
            logger.info("Scheduler shut down successfully")
        else:
            logger.info("Scheduler not running; nothing to shut down")
    except Exception:
        logger.error("Scheduler shutdown failed", exc_info=True)
from app.config.database import SessionLocal
from app.models import device as device_models
from app.services import snmp_collector

scheduler = AsyncIOScheduler()

def poll_all_devices():
    """
    Fetch all devices from DB and trigger collection for each.
    """
    # Create a new session for this job thread/context
    db = SessionLocal()
    try:
        devices = db.query(device_models.Device).all()
        print(f"Scheduler: Found {len(devices)} devices to poll.")
        for device in devices:
            # We could use a worker pool here, but for 'basic', serial loop is fine or relying on async nature if we made collector async.
            # Since collector is effectively sync (requests + pysnmp), this blocking loop might block the scheduler thread.
            # Ideally: submit to executor. For now: direct call.
            try:
                snmp_collector.collect_metrics(device)
            except Exception as e:
                print(f"Error polling device {device.name}: {e}")
    except Exception as e:
        print(f"Scheduler Error: {e}")
    finally:
        db.close()

def start_scheduler():
    # Add job to run every 1 minute
    scheduler.add_job(poll_all_devices, 'interval', minutes=1)
    
    # Add anomaly detection job every 2 minutes
    from app.services import anomaly_service
    scheduler.add_job(anomaly_service.run_anomaly_checks, 'interval', minutes=2)
    
    scheduler.start()
    print("Scheduler started...")
