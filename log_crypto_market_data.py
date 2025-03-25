from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import time

from coin_market_cap_client.client import CoinMarketCapClient
from coin_market_cap_client import envs
from coin_market_cap_client.currency_symbols import Currency

topic_name = "btc_price"

kafka_config = {
    "bootstrap.servers": "localhost:9092"
}
producer = Producer(kafka_config)
admin_kafka = AdminClient(kafka_config)
if topic_name not in list(admin_kafka.list_topics().topics.keys()):
    admin_kafka.create_topics(new_topics=[NewTopic(topic=topic_name)])

with open("./secrets/coin-market-cap-api-key.txt", "r") as file:
    api_key = file.read()
client = CoinMarketCapClient(api_key, envs.PROD)

try:
    while True:
        quote = client.get_latest_price(from_symbol=Currency.BTC, to_symbols=[Currency.USD])
        producer.produce(topic=topic_name, value=f"{quote.model_dump_json()}", key=Currency.BTC.value)
        producer.poll()
        time.sleep(20)
except KeyboardInterrupt:
    print("stopping...")



