from pysnmp.hlapi import *
import requests
import os
import random
from app.config.logging import get_logger

logger = get_logger(__name__)

OID_CPU_LOAD_1MIN = '1.3.6.1.4.1.2021.10.1.3.1'
OID_MEMORY_TOTAL = '1.3.6.1.4.1.2021.4.5.0'
OID_MEMORY_FREE = '1.3.6.1.4.1.2021.4.6.0'


def get_snmp_value(ip, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1),
        UdpTransportTarget((ip, 161), timeout=1, retries=0),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication or errorStatus:
        return None

    for varBind in varBinds:
        return varBind[1]

    return None


def collect_metrics(device):
    logger.info(f"Collecting metrics: device={device.name} ip={device.ip_address}")

    cpu_val = get_snmp_value(device.ip_address, "public", OID_CPU_LOAD_1MIN)

    if cpu_val is None:
        logger.warning(f"SNMP failed; using mock data: device={device.name}")
        cpu_val = random.uniform(10, 80)
        mem_val = random.uniform(20, 90)
    else:
        try:
            cpu_val = float(cpu_val)
        except Exception:
            cpu_val = 0.0

        total_mem = get_snmp_value(device.ip_address, "public", OID_MEMORY_TOTAL)
        free_mem = get_snmp_value(device.ip_address, "public", OID_MEMORY_FREE)
        if total_mem and free_mem:
            mem_val = ((int(total_mem) - int(free_mem)) / int(total_mem)) * 100
        else:
            mem_val = 0.0

    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    post_url = f"{backend_url}/metrics/post"

    metrics_to_push = [
        {"metric_name": "cpu_usage", "value": cpu_val},
        {"metric_name": "memory_usage", "value": mem_val},
    ]

    for m in metrics_to_push:
        payload = {
            "device_id": device.id,
            "metric_name": m["metric_name"],
            "value": float(m["value"]),
        }
        try:
            r = requests.post(post_url, json=payload, timeout=5)
            logger.info(
                f"Metric pushed: device_id={device.id} metric={m['metric_name']} status={r.status_code}"
            )
        except Exception:
            logger.error(f"Failed to push metric: device_id={device.id} metric={m['metric_name']}", exc_info=True)
