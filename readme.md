# Kafka intro project - realtime BTC price raw and aggregated

objective: try out kafka and spark structured streaming.

1. Data Source: real-time BTC price data
2. Kafka Cluster: Streams BTC price data to a Kafka topic.
3. Consumer (PySpark Structured Streaming): Reads data from Kafka and processes BTC price trends.
4. Data Storage: Stores results in AWS S3 (raw data)

## How to run:
1. get API key from https://pro.coinmarketcap.com/login/
2. put the API key in secrets/coin-market-cap-api-key.txt
3. start kafka service
```bash
docker-compose up -d
```
4. start pushing btc price events into topic
```bash
python log_crypto_market_data.py
```
5. start consuming events from topic and saving to s3 location
> make sure you have your aws API access key set up
```bash
./start_spark_process_job.sh
```
6. start spark shell to read results
``` bash 
pyspark --packages org.apache.hadoop:hadoop-aws:3.3.6
```
