import random
from datetime import datetime, timedelta
import pandas as pd

Num_Rows = 2000

commodities = {
    "Avocados": {"temp": (4, 8), "humidity": (85, 95)},
    "Bananas": {"temp": (12, 15), "humidity": (80, 90)},
    "Mangoes": {"temp": (8, 13), "humidity": (80, 90)},
    "Grapes": {"temp": (0, 4), "humidity": (90, 95)},
    "Apples": {"temp": (0, 4), "humidity": (85, 90)},
    "Tomatoes": {"temp": (12, 18), "humidity": (70, 85)},
    "Oranges": {"temp": (3, 8), "humidity": (80, 90)},
    "Potatoes": {"temp": (5, 10), "humidity": (85, 95)}
}

routes = [
    ("Hyderabad", "Mumbai"),
    ("Hyderabad", "Chennai"),
    ("Bengaluru", "Delhi"),
    ("Vizag", "Mumbai"),
    ("Pune", "Kolkata"),
    ("Nagpur", "Chennai")
]

# Approximate GPS coordinates
city_coords = {
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Delhi": (28.7041, 77.1025),
    "Vizag": (17.6868, 83.2185),
    "Pune": (18.5204, 73.8567),
    "Kolkata": (22.5726, 88.3639),
    "Nagpur": (21.1458, 79.0882)
}

start_time = datetime.now()

records = []

for i in range(Num_Rows):

    commodity = random.choice(list(commodities.keys()))

    temp_range = commodities[commodity]["temp"]
    hum_range = commodities[commodity]["humidity"]

    origin, destination = random.choice(routes)

    lat, lon = city_coords[origin]

    # Add small GPS variation
    latitude = round(lat + random.uniform(-0.25, 0.25), 5)
    longitude = round(lon + random.uniform(-0.25, 0.25), 5)

    temperature = round(random.uniform(*temp_range), 2)
    humidity = round(random.uniform(*hum_range), 2)
    vibration = round(random.uniform(0.0, 2.0), 2)
    pressure = round(random.uniform(995, 1025), 2)
    battery = random.randint(65, 100)
    speed = round(random.uniform(0, 90), 2)

    door_status = random.choice(["Closed", "Closed", "Closed", "Open"])
    light_detected = door_status == "Open"

    # spoilage formula
    spoilage = (
        abs(temperature - sum(temp_range)/2) * 0.08 +
        vibration * 0.15 +
        (100 - humidity) * 0.004
    )

    spoilage = round(min(spoilage, 1.0), 2)

    if spoilage < 0.30:
        alert = "Normal"
    elif spoilage < 0.60:
        alert = "Warning"
    else:
        alert = "Critical"

    sensor_status = random.choice(["Healthy"] * 9 + ["Faulty"])

    records.append({
        "timestamp": (start_time + timedelta(seconds=i*5)).strftime("%Y-%m-%d %H:%M:%S"),
        "container_id": f"CNT{random.randint(1,25):03}",
        "shipment_id": f"SHP{1000+i}",
        "commodity": commodity,
        "origin": origin,
        "destination": destination,
        "latitude": latitude,
        "longitude": longitude,
        "temperature": temperature,
        "humidity": humidity,
        "vibration": vibration,
        "pressure": pressure,
        "battery_level": battery,
        "door_status": door_status,
        "light_detected": light_detected,
        "gps_speed": speed,
        "spoilage_index": spoilage,
        "sensor_status": sensor_status,
        "alert_level": alert
    })

df = pd.DataFrame(records)

df.to_csv("container_telemetry3.csv", index=False)

print(df.head())
