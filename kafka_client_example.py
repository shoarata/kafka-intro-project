from confluent_kafka import Consumer
from config import btc_price_topic_name
config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "dummy.consumer",
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(config)
consumer.subscribe([btc_price_topic_name])

while True:
    try:
        msg = consumer.poll(2)
        if msg is None:
            print("no messages, waiting...")
        elif msg.error():
            print(f"ERROR: {msg.error()}")
        else:
            print(f"Consumed event: {msg.topic()=}, {msg.key()=}, {msg.value()=}")

    except KeyboardInterrupt:
        print("closing connection...")
        break
consumer.close()