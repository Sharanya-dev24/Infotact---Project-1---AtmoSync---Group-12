import json
import time
import pandas as pd
from kafka import KafkaProducer

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# Read the CSV file
# df = pd.read_csv("container_telemetry.csv")   # Change the filename if needed
df = pd.read_csv("data/container_telemetry.csv")
# Send each row to Kafka
for _, row in df.iterrows():
    producer.send("container_telemetry", row.to_dict())
    print(f"Sent: {row['container_id']}")
    time.sleep(1)   # Send one record every second

producer.flush()
producer.close()

print("Finished sending all records.")
