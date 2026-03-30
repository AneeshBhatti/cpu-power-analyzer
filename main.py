import csv
import os
import argparse
import threading
import time

from monitor import collect_metrics
from workload import run_idle, run_stress
from analysis import load_csv, summarize_metrics, detect_anomalies, print_report

def save_to_csv(samples, output_file):
    os.makedirs("logs", exist_ok=True)

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["timestamp", "cpu_percent", "memory_percent", "load_avg", "cpu_count",]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(samples)

def run_monitoring(duration):
    samples = []
    for _ in range(duration):
        metrics = collect_metrics()
        samples.append(metrics)
        print(metrics)
    return samples

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["idle", "stress"], required=True)
    parser.add_argument("--duration", type=int, default=10)
    args = parser.parse_args()

    if args.mode == "idle":
        workload = run_idle
    else:
        workload = run_stress
    
    print(f"Running {args.mode} mode for {args.duration} seconds")

    workload_thread = threading.Thread(target=workload, args=(args.duration,))
    workload_thread.start()

    samples = run_monitoring(args.duration)

    workload_thread.join()

    output_file = f"logs/{args.mode}_run_{int(time.time())}.csv"
    save_to_csv(samples, output_file)

    print(f"\nSaved to {output_file}")

    rows = load_csv(output_file)
    summary = summarize_metrics(rows)
    anomalies = detect_anomalies(summary, args.mode)
    print_report(args.mode, summary, anomalies)

if __name__ == "__main__":
    main()