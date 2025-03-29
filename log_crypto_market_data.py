from confluent_kafka import Producer
from config import btc_price_topic_name
from confluent_kafka.admin import AdminClient, NewTopic
import time

from coin_market_cap_client.client import CoinMarketCapClient
from coin_market_cap_client import envs
from coin_market_cap_client.currency_symbols import Currency
from schemas import ProducerBTCPrice


kafka_config = {
    "bootstrap.servers": "localhost:9092"
}
producer = Producer(kafka_config)
admin_kafka = AdminClient(kafka_config)
if btc_price_topic_name not in list(admin_kafka.list_topics().topics.keys()):
    admin_kafka.create_topics(new_topics=[NewTopic(topic=btc_price_topic_name)])

with open("./secrets/coin-market-cap-api-key.txt", "r") as file:
    api_key = file.read()
client = CoinMarketCapClient(api_key, envs.PROD)

try:
    while True:
        quote = client.get_latest_price(from_symbol=Currency.BTC, to_symbols=[Currency.USD])
        usd_quote = quote.quotes[0]
        btc_price = ProducerBTCPrice(last_updated=usd_quote.last_updated, btc_price_usd=usd_quote.price)
        producer.produce(topic=btc_price_topic_name, value=f"{btc_price.model_dump_json()}", key=Currency.BTC.value, callback=lambda err, msg: print(str(msg.value())))
        producer.poll()
        time.sleep(20)
except KeyboardInterrupt:
    print("stopping...")



