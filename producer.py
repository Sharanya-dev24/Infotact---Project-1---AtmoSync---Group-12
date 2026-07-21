import json
from kafka import KafkaProducer

# Kafka Configuration
KAFKA_TOPIC = "container-telemetry"
BOOTSTRAP_SERVER = "localhost:9092"

# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

print("Kafka Producer Connected!")

def send_to_kafka(telemetry):
    try:
        producer.send(KAFKA_TOPIC, value=telemetry)
        producer.flush()

        print(
            f"Sent -> "
            f"Shipment: {telemetry['shipment_id']} | "
            f"Container: {telemetry['container_id']} | "
            f"Temperature: {telemetry['temperature']}°C | "
            f"Humidity: {telemetry['humidity']}% | "
            f"Alert: {telemetry['alert_level']}"
        )

    except Exception as e:
        print(f"Error sending message: {e}")

# Close Kafka Producer
def close_producer():
    producer.flush()
    producer.close()
    print("Kafka Producer Closed.")
