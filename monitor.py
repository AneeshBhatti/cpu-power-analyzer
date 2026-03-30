import time
import psutil
import os

def collect_metrics():
    return {
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "cpu_count": os.cpu_count(),
        "load_avg": psutil.getloadavg()[0] if hasattr(psutil, "getloadavg") else 0,
    }