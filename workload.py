import time
import multiprocessing
import math

def cpu_burn(duration):
    end_time = time.time() + duration
    x = 0.0001
    while time.time() < end_time:
        x = math.sqrt(x + 1.2345)

def run_stress(duration):
    processes = []
    cpu_count = multiprocessing.cpu_count()

    for _ in range(cpu_count):
        p = multiprocessing.Process(target=cpu_burn, args=(duration,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

def run_idle(duration):
    time.sleep(duration)