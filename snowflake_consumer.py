import json
from kafka import KafkaConsumer
from snowflake_connection import get_connection


# Kafka Consumer
consumer = KafkaConsumer(
    "container-telemetry",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    group_id="snowflake-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)


# Snowflake Connection
conn = get_connection()

cursor = conn.cursor()
print("Listening for Kafka messages...")


for message in consumer:

    data = message.value

    print("Received:")
    print(data)

    sql = """
    INSERT INTO IOT_STREAM
    (
    CLOCK_TIMESTAMP,
    SIMULATED_TIMESTAMP,
    CONTAINER_ID,
    SHIPMENT_ID,
    COMMODITY,
    ORIGIN,
    DESTINATION,
    LATITUDE,
    LONGITUDE,
    TEMPERATURE,
    HUMIDITY,
    VIBRATION,
    PRESSURE,
    BATTERY_LEVEL,
    DOOR_STATUS,
    LIGHT_DETECTED,
    GPS_SPEED,
    SPOILAGE_INDEX,
    SENSOR_STATUS,
    ALERT_LEVEL
    )

    VALUES
    (
    TO_TIMESTAMP(%(clock_timestamp)s, 'YYYY-MM-DD HH24:MI:SS'),
    TO_TIMESTAMP(%(simulated_timestamp)s, 'YYYY-MM-DD HH24:MI:SS'),
    %(container_id)s,
    %(shipment_id)s,
    %(commodity)s,
    %(origin)s,
    %(destination)s,
    %(latitude)s,
    %(longitude)s,
    %(temperature)s,
    %(humidity)s,
    %(vibration)s,
    %(pressure)s,
    %(battery_level)s,
    %(door_status)s,
    %(light_detected)s,
    %(gps_speed)s,
    %(spoilage_index)s,
    %(sensor_status)s,
    %(alert_level)s
    )
    """

    # Convert producer JSON keys to Snowflake table keys
    snowflake_data = {

        "clock_timestamp": data["clock_timestamp"],
        "simulated_timestamp": data["simulated_timestamp"],
        "container_id": data["container_id"],
        "shipment_id": data["shipment_id"],

        "commodity": data["commodity"],

        "origin": data["origin"],
        "destination": data["destination"],

        "latitude": data["latitude"],
        "longitude": data["longitude"],

        "temperature": data["temperature"],
        "humidity": data["humidity"],

        "vibration": data["vibration"],
        "pressure": data["pressure"],

        "battery_level": data["battery_level"],

        "door_status": data["door_status"],
        "light_detected": data["light_detected"],

        "gps_speed": data["gps_speed"],

        "spoilage_index": data["spoilage_index"],

        "sensor_status": data["sensor_status"],

        "alert_level": data["alert_level"]
    }


    try:

        cursor.execute(
            sql,
            snowflake_data
        )

        conn.commit()

        print(
            "Inserted:",
            data["container_id"]
        )

    except Exception as e:

        print("Snowflake Error:")
        print(e)

print("\nData successfully transferred to Snowflake.")