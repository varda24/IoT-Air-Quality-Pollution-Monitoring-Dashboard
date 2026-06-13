import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import os

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Auto refresh every 10 seconds
st_autorefresh(interval=10000, key="refresh")

# --------------------------------
# LOAD DATA
# --------------------------------

csv_path = "data/air_quality_log.csv"

if not os.path.exists(csv_path):
    st.error("CSV file not found.")
    st.stop()

df = pd.read_csv(csv_path)

if len(df) == 0:
    st.warning("No sensor data available.")
    st.stop()

latest = df.iloc[-1]

aqi = int(latest["AQI"])
temp = float(latest["Temperature"])
humidity = float(latest["Humidity"])
status = latest["Status"]

# --------------------------------
# HEADER
# --------------------------------

st.title("🌍 IoT Air Quality & Pollution Monitoring Dashboard")

st.markdown(
    """
    Real-time environmental monitoring using ESP32, DHT22,
    MQ135 Simulation, ThingSpeak and Streamlit.
    """
)

st.divider()

# --------------------------------
# AQI STATUS
# --------------------------------

if aqi <= 50:
    color = "green"

elif aqi <= 100:
    color = "yellow"

elif aqi <= 200:
    color = "orange"

else:
    color = "red"

# --------------------------------
# KPI CARDS
# --------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("AQI", aqi)
c2.metric("Temperature", f"{temp:.1f} °C")
c3.metric("Humidity", f"{humidity:.1f} %")
c4.metric("Status", status)

# --------------------------------
# --------------------------------
# Professional Sidebar
# --------------------------------
st.sidebar.title("System Information")
st.sidebar.success("ESP32 Connected")
st.sidebar.write("PlatformIO")
st.sidebar.write("Wokwi Simulation")
st.sidebar.write("ThingSpeak Cloud")
st.sidebar.write("Streamlit Dashboard")
st.sidebar.metric(
    "Total Records",
    len(df)
)

# --------------------------------
# AQI GAUGE (small)
# --------------------------------
gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={"text": "AQI"},
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={
            "axis": {"range": [0, 500]},
            "steps": [
                {"range": [0, 50], "color": "#00cc66"},
                {"range": [50, 100], "color": "#ffcc00"},
                {"range": [100, 200], "color": "#ff9900"},
                {"range": [200, 500], "color": "#ff3300"},
            ]
        }
    )
)

# update layout already set for `gauge`
# show gauge and pollution pie side-by-side
top_left, top_right = st.columns(2)

with top_left:
    st.plotly_chart(
        gauge,
        use_container_width=True
    )

with top_right:
    status_counts = df["Status"].value_counts()

    pie = px.pie(
        names=status_counts.index,
        values=status_counts.values,
        hole=0.5,
        title="Pollution Distribution"
    )

    pie.update_layout(height=300)

    st.plotly_chart(
        pie,
        use_container_width=True
    )

# --------------------------------
# ALERT BOX
# --------------------------------

if status == "GOOD":
    st.success("Air Quality is Safe")

elif status == "MODERATE":
    st.warning("Moderate Air Pollution Detected")

elif status == "POOR":
    st.warning("Poor Air Quality. Avoid prolonged exposure.")

else:
    st.error("Hazardous Pollution Level Detected!")

# --------------------------------
# Compact Trend Charts
# --------------------------------

row1_col1, row1_col2 = st.columns(2)

with row1_col1:

    fig_aqi = px.line(
        df,
        x="Timestamp",
        y="AQI",
        title="AQI Trend"
    )

    fig_aqi.update_layout(height=300)

    st.plotly_chart(
        fig_aqi,
        use_container_width=True
    )

with row1_col2:

    fig_temp = px.line(
        df,
        x="Timestamp",
        y="Temperature",
        title="Temperature Trend"
    )

    fig_temp.update_layout(height=300)

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )

# --------------------------------
# Humidity + Latest Records
# --------------------------------

row2_col1, row2_col2 = st.columns(2)

with row2_col1:

    fig_humidity = px.line(
        df,
        x="Timestamp",
        y="Humidity",
        title="Humidity Trend"
    )

    fig_humidity.update_layout(height=300)

    st.plotly_chart(
        fig_humidity,
        use_container_width=True
    )

with row2_col2:

    st.subheader("Latest Records")

    st.dataframe(
        df.tail(10),
        height=300,
        use_container_width=True
    )

# --------------------------------
# AQI TABLE (moved to expander)
# --------------------------------

aqi_table = pd.DataFrame(
    {
        "AQI Range": [
            "0 - 50",
            "51 - 100",
            "101 - 200",
            "201 - 500"
        ],
        "Category": [
            "Good",
            "Moderate",
            "Poor",
            "Hazardous"
        ]
    }
)

with st.expander("AQI Classification Guide"):
    st.table(aqi_table)

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "ESP32 • PlatformIO • Wokwi • ThingSpeak • Streamlit"
)