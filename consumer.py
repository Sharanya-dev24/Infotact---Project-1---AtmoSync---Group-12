import json
from kafka import KafkaConsumer

# Connect to Kafka
consumer = KafkaConsumer(
    "container-telemetry",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Waiting for messages...\n")

for message in consumer:
    print(message.value)
