import random
from datetime import datetime, timedelta
import pandas as pd
import time

from producer import send_to_kafka, close_producer

routes = pd.read_csv("routes1.csv")

# CITY COORDINATES
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

# COMMODITY CONDITIONS
commodity_conditions = {
    "Avocados": {"temp": (4, 8), "humidity": (85, 95)},
    "Bananas": {"temp": (12, 15), "humidity": (80, 90)},
    "Mangoes": {"temp": (8, 13), "humidity": (80, 90)},
    "Grapes": {"temp": (0, 4), "humidity": (90, 95)},
    "Apples": {"temp": (0, 4), "humidity": (85, 90)},
    "Tomatoes": {"temp": (12, 18), "humidity": (70, 85)},
    "Oranges": {"temp": (3, 8), "humidity": (80, 90)},
    "Potatoes": {"temp": (5, 10), "humidity": (85, 95)}
}

for index, route in routes.iterrows():

    origin = route["origin"]
    destination = route["destination"]
    distance_km = route["distance_km"]

    latitude, longitude = city_coords[origin]

    commodity = random.choice(list(commodity_conditions.keys()))

    shipment_id = f"SHP{1001 + index}"
    container_id = f"CNT{index + 1:03}"

    temp_range = commodity_conditions[commodity]["temp"]
    humidity_range = commodity_conditions[commodity]["humidity"]

    average_speed = random.randint(45, 55)

    travel_hours = distance_km / average_speed

    clock_interval = 0.2         # Send one record every 0.2 real seconds
    simulation_interval = 30         # Each record represents 30 minutes of travel

    travel_minutes = int(travel_hours * 60)

    total_readings = travel_minutes // simulation_interval

    print("---------------------------------------")
    print("Shipment :", shipment_id)
    print("Container:", container_id)
    print(origin, "->", destination)
    print("Commodity:", commodity)
    print("Distance:", distance_km, "km")
    print("Speed:", average_speed, "km/hr")
    print("Travel Hours:", round(travel_hours, 2))
    print("Compression: 15 simulated minutes every 5 seconds")
    print("Telemetry Records:", total_readings)

    start_time = datetime.now()

    temperature = round(random.uniform(*temp_range), 2)
    humidity = round(random.uniform(*humidity_range), 2)
    vibration = 0.20
    battery = 100

    for i in range(total_readings):

        clock_timestamp = datetime.now()

        simulated_timestamp = start_time + timedelta(
            minutes=i * simulation_interval
        )
        temperature += random.uniform(-0.15, 0.20)
        humidity += random.uniform(-0.6, 0.6)
        vibration += random.uniform(-0.03, 0.03)

        temperature = max(temp_range[0], min(temp_range[1] + 2, temperature))
        humidity = max(70, min(98, humidity))
        vibration = max(0, round(vibration, 2))

        pressure = round(random.uniform(995, 1025), 2)

        battery = max(20, battery - 0.01)

        speed = round(random.uniform(average_speed - 3, average_speed + 3), 2)

        latitude += random.uniform(0.001, 0.005)
        longitude += random.uniform(-0.005, 0.001)

        door_status = "Closed"

        if random.random() < 0.02:
            door_status = "Open"

        light_detected = door_status == "Open"

        ideal_temp = (temp_range[0] + temp_range[1]) / 2

        spoilage = (
            abs(temperature - ideal_temp) * 0.08 +
            vibration * 0.15 +
            (100 - humidity) * 0.004
        )

        spoilage = round(min(spoilage, 1), 2)

        if spoilage < 0.30:
            alert = "Normal"
        elif spoilage < 0.60:
            alert = "Warning"
        else:
            alert = "Critical"

        telemetry = {

            "clock_timestamp": clock_timestamp.strftime("%Y-%m-%d %H:%M:%S"),

            "simulated_timestamp": simulated_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "container_id": container_id,
            "shipment_id": shipment_id,

            "commodity": commodity,

            "origin": origin,
            "destination": destination,

            "latitude": round(latitude, 5),
            "longitude": round(longitude, 5),

            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),

            "vibration": vibration,
            "pressure": pressure,

            "battery_level": round(battery, 2),

            "door_status": door_status,
            "light_detected": light_detected,

            "gps_speed": speed,

            "spoilage_index": spoilage,

            "sensor_status": "Healthy",

            "alert_level": alert
        }
        

        print(
            f"Sent -> "
            f"{shipment_id} | "
            f"{container_id} | "
            f"{round(temperature,2)}°C | "
            f"{round(humidity,2)}% | "
            f"{alert}"
        )
        send_to_kafka(telemetry)
        time.sleep(clock_interval)


close_producer()

print("\nLive telemetry streaming completed!")
