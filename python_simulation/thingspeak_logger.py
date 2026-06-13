import random
import time
import requests
import pandas as pd
from datetime import datetime
import os

WRITE_API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY"

os.makedirs("data", exist_ok=True)

csv_file = "data/air_quality_log.csv"

logs = []

while True:

    aqi = random.randint(0, 500)
    temperature = round(random.uniform(22, 40), 2)
    humidity = round(random.uniform(35, 85), 2)

    if aqi <= 50:
        status = "GOOD"
        alert = "SAFE"
        status_code = 1
        alert_code = 0

    elif aqi <= 100:
        status = "MODERATE"
        alert = "CAUTION"
        status_code = 2
        alert_code = 1

    elif aqi <= 200:
        status = "POOR"
        alert = "WARNING"
        status_code = 3
        alert_code = 2

    else:
        status = "HAZARDOUS"
        alert = "DANGER"
        status_code = 4
        alert_code = 3

    url = "https://api.thingspeak.com/update"

    payload = {
        "api_key": WRITE_API_KEY,
        "field1": aqi,
        "field2": temperature,
        "field3": humidity,
        "field4": status_code,
        "field5": alert_code
    }

    response = requests.get(url, params=payload)

    print("=" * 40)
    print("Status Code:", response.status_code)
    print("ThingSpeak Response:", response.text)

    logs.append([
        datetime.now(),
        aqi,
        temperature,
        humidity,
        status,
        alert
    ])

    df = pd.DataFrame(
        logs,
        columns=[
            "Timestamp",
            "AQI",
            "Temperature",
            "Humidity",
            "Status",
            "Alert"
        ]
    )

    df.to_csv(csv_file, index=False)

    print("CSV Updated")

    time.sleep(20)