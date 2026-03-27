from monitor import collect_metrics

def main():
    for _ in range(5):
        metrics = collect_metrics()
        print(metrics)

if __name__ == "__main__":
    main()