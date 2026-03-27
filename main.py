import csv
import os

from monitor import collect_metrics

def save_to_csv(samples, output_file):
    os.makedirs("logs", exist_ok=True)

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["timestamp", "cpu_percent", "memory_percent"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(samples)

def main():
    samples = []

    for _ in range(5):
        metrics = collect_metrics()
        samples.append(metrics)
        print(metrics)
    
    output_file = "logs/system_metrics.csv"
    save_to_csv(samples, output_file)
    print(f"\nSaved metrics to {output_file}")

if __name__ == "__main__":
    main()