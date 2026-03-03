from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'patient_vitals',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Listening to live patient vitals...\n")

for message in consumer:
    data = message.value
    print("RECEIVED:", data)