from confluent_kafka import Producer
import time

config = {
    "bootstrap.servers": "localhost:9092"
}
producer = Producer(config)
def del_callback(err, msg):
    if err:
        print(f"{err=}")
    else:
        print(f"{msg.topic()=}, {msg.key()=}, {msg.value()=}")
for i in range (10):
    time.sleep(2)
    producer.produce(topic="system_logs", value=f"this is a test log {i}", key="ShoArata", callback=del_callback)
producer.flush()

