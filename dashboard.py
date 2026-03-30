import time
import psutil
import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

from analysis import summarize_metrics, detect_anomalies

st.set_page_config(page_title="CPU Monitor Dashboard", layout="wide")
st.title("CPU Power & Performance Dashboard")

# Session state keeps monitoring data across Stremlit reruns
if "data" not in st.session_state:
    st.session_state["data"] = []

if "monitoring" not in st.session_state:
    st.session_state["monitoring"] = False

if "selected_mode" not in st.session_state:
    st.session_state["selected_mode"] = "idle"

refresh_rate = st.slider("Refresh Rate (seconds)", 1, 5, 1)

selected_mode = st.selectbox(
    "Monitoring Context",
    ["idle", "stress"],
    index=0 if st.session_state["selected_mode"] == "idle" else 1,
)
st.session_state["selected_mode"] = selected_mode

col_a, col_b, col_c = st.columns(3)

# Start a new monitoring session and clear any prior run data
if col_a.button("Start Monitoring"):
    st.session_state["data"] = []
    st.session_state["monitoring"] = True

# Stop sampling but keep collected data visible for summary review
if col_b.button("Stop Monitoring"):
    st.session_state["monitoring"] = False

# Clear stored samples entirely
if col_c.button("Clear Data"):
    st.session_state["data"] = []
    st.session_state["monitoring"] = False

st.write(f"Monitoring active: {'Yes' if st.session_state['monitoring'] else 'No'}")

# While monitoring is enabled, refresh automatically and append new samples
if st.session_state["monitoring"]:
    st_autorefresh(interval=refresh_rate * 1000, key="monitor_refresh")

    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent
    load = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
    cpu_count = os.cpu_count() or 0

    st.session_state["data"].append({
        "timestamp": time.time(),
        "cpu_percent": cpu,
        "memory_percent": memory,
        "load_avg": load,
        "cpu_count": cpu_count
    })

if st.session_state["data"]:
    df = pd.DataFrame(st.session_state["data"])
    latest = df.iloc[-1]
    
    st.subheader("Live Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CPU %", f"{latest['cpu_percent']:.1f}%")
    col2.metric("Memory %", f"{latest['memory_percent']:.1f}%")
    col3.metric("Load Avg", f"{latest['load_avg']:.2f}")
    col4.metric("CPU Count", int(latest['cpu_count']))
    
    # Plot CPU, memory, and laod average over time
    chart_df = df[["timestamp", "cpu_percent", "memory_percent", "load_avg"]].copy()
    chart_df["timestamp"] = pd.to_datetime(chart_df["timestamp"], unit="s")
    chart_df = chart_df.set_index("timestamp")
    st.line_chart(chart_df)

    # Show summary and anomaly results after monitoring stops
    if not st.session_state["monitoring"]:
        rows = df.to_dict(orient="records")
        summary = summarize_metrics(rows)
        anomalies = detect_anomalies(summary, mode=st.session_state["selected_mode"])

        st.subheader("Run Summary")
        st.write(f"Selected mode: {st.session_state['selected_mode']}")
        st.write(f"Samples collected: {summary['samples']}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg CPU %", summary["avg_cpu_percent"])
        col2.metric("Max CPU %", summary["max_cpu_percent"])
        col3.metric("Avg Memory %", summary["avg_memory_percent"])
        col4.metric("Max Memory %", summary["max_memory_percent"])

        if "cpu_stddev" in summary:
            st.write(f"CPU Std Dev: {summary['cpu_stddev']}")

        st.subheader("Anomalies")
        if anomalies:
            for anomaly in anomalies:
                st.warning(anomaly)
        else:
            st.success("No anomalies detected")
    
else:
    st.info("No samples collected yet.")
