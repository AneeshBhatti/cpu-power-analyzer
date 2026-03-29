import time
import psutil
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CPU Monitor Dashboard", layout="wide")

st.title("CPU Power & Performance Dashboard")

refresh_rate = st.slider("Refresh Rate (seconds)", 1, 5, 1)

run = st.checkbox("Start Monitoring")

data = []

placeholder = st.empty()

while run:
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent
    load = psutil.getloadavg()[0] if hasattr(psutil, "getloadavg") else 0

    data.append({
        "time": time.time(),
        "cpu": cpu,
        "memory": memory,
        "load": load
    })

    df = pd.DataFrame(data)

    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        col1.metric("CPU %", f"{cpu}%")
        col2.metric("Memory %", f"{memory}%")
        col3.metric("Load Avg", round(load, 2))

        st.line_chart(df.set_index("time"))

    time.sleep(refresh_rate)