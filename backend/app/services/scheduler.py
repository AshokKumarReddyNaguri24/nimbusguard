from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
