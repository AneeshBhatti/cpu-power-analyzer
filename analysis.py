import csv
import statistics

def load_csv(filepath):
    rows = []
    with open(filepath, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append({
                "timestamp": float(row["timestamp"]),
                "cpu_percent": float(row["cpu_percent"]),
                "memory_percent": float(row["memory_percent"]),
                "cpu_count": int(row["cpu_count"]) if "cpu_count" in row and row["cpu_count"] else None,
                "load_avg": float(row["load_avg"]) if "load_avg" in row and row["load_avg"] else None,
            })
    return rows

def summarize_metrics(rows):
    cpu_values = [row["cpu_percent"] for row in rows]
    mem_values = [row["memory_percent"] for row in rows]

    summary = {
        "samples": len(rows),
        "avg_cpu_percent": round(statistics.mean(cpu_values), 2),
        "max_cpu_percent": round(max(cpu_values), 2),
        "avg_memory_percent": round(statistics.mean(mem_values), 2),
        "max_memory_percent": round(max(mem_values), 2),
    }

    if len(cpu_values) > 1:
        summary["cpu_stddev"] = round(statistics.pstdev(cpu_values), 2)
    else:
        summary["cpu_stddev"] = 0.0

    return summary

def detect_anomalies(summary, mode):
    anomalies = []

    if mode == "idle" and summary["max_cpu_percent"] > 95:
        anomalies.append("Unexpected CPU usage spike during idle")

    if mode == "stress" and summary["avg_cpu_percent"] < 35:
        anomalies.append("Stress workload produced unexpectedly low average CPU usage")

    if mode == "idle" and summary["avg_cpu_percent"] > 40:
        anomalies.append("Idle workload showed unexpectedly high average CPU usage")
    
    return anomalies

def print_report(mode, summary, anomalies):
    print("\n===== Analysis Report =====")
    print(f"Mode: {mode}")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\nAnomalies:")
    if anomalies:
        for anomaly in anomalies:
            print(f"- {anomaly}")
    else:
        print("- None detected")

def compare_modes(idle_file, stress_file):
    idle = load_csv(idle_file)
    stress = load_csv(stress_file)

    idle_summary = summarize_metrics(idle)
    stress_summary = summarize_metrics(stress)

    print("\n===== Comparison =====")
    print(f"Idle Avg CPU: {idle_summary['avg_cpu_percent']}%")
    print(f"Stress Avg CPU: {stress_summary['avg_cpu_percent']}%")

    diff = stress_summary['avg_cpu_percent'] - idle_summary['avg_cpu_percent']
    print(f"CPU Increase: {round(diff, 2)}%")