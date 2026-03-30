# CPU Power & Performance Validation Dashboard

A Python-based system-level validation tool for analyzing CPU behavior under controlled workloads.  
This project enables real-time monitoring, workload-driven testing, and post-run performance analysis.

---

## Overview

This tool was built to explore how CPU performance changes under different workload conditions.  
It supports both **idle** and **stress** modes, collects system metrics, and provides both:

- CLI-based validation reports
- A real-time dashboard for visualization

---

## Features

- **Workload Modes**
  - Idle mode (baseline system behavior)
  - Stress mode (full CPU utilization using multiprocessing)

- **System Metrics Collection**
  - CPU utilization
  - Memory usage
  - Load average
  - CPU core count

- **Logging & Analysis**
  - CSV-based logging for reproducible runs
  - Summary statistics (avg, max, std dev)
  - Workload-aware anomaly detection

- **Real-Time Dashboard**
  - Built with Streamlit
  - Live metric updates
  - Time-series visualization
  - Post-run summaries and anomaly reporting

---

##  Design

The project is structured into modular components:

- `main.py` — Runs workload tests and generates validation reports  
- `monitor.py` — Collects system metrics  
- `workload.py` — Implements idle and stress workloads  
- `analysis.py` — Computes summaries and detects anomalies  
- `dashboard.py` — Real-time visualization using Streamlit  

---

![Dashboard] (assets/dashboard.png)
## Usage

### Install dependencies
pip install -r requirements.txt

### Run validation tests (CLI)
Idle mode:
- python3 main.py --mode idle --duration 10

Stress mode:
- python3 main.py --mode stress --duration 10

Outputs:
- CSV logs stored in logs/
- Summary statistics and anomaly report printed in terminal

Run Dashboard:
- python3 -m streamlit run dashboard.py

Then:
1. Select monitoring context (idle or stress)
2. Click Start Monitoring
3. Optionally run workload in another terminal
4. Click Stop Monitoring to view summary results

## Example Results

Typical stress run output:

- Average CPU utilization: ~95–100%
- Low variance during sustained load
- Clear transition between idle and stress phases

Typical idle run output:

- Low CPU utilization (~10–30%)
- Stable behavior with minimal variance

Dashboard visualization shows:
- Real-time CPU usage spikes during stress
- Clear separation between idle and load conditions

## Key Insights

- CPU utilization under stress can show brief drops due to scheduling and sampling timing
- Initial anomaly detection flagged expected stress behavior, requiring refinement of detection logic
- Workload-aware analysis is critical to distinguishing expected vs abnormal system behavior
- Real-time monitoring introduces sampling variability compared to controlled CLI runs