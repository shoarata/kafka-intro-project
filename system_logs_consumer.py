from confluent_kafka import Consumer
config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "dummy.consumer"

}
consumer = Consumer(config)
consumer.subscribe(["system_logs"])

while True:
    try:
        msg = consumer.poll(1)
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