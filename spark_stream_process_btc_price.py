from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from config import btc_price_topic_name
from schemas import ConsumerBTCPrice

spark = SparkSession.builder.appName("btc_price_stream").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
btc_price_stream = spark.readStream.format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", btc_price_topic_name)\
    .option("startingOffsets", "earliest") \
    .load()

btc_price_df = btc_price_stream.selectExpr("CAST(value as STRING) as btc_price_json")\
    .withColumn("parsed_json", F.from_json(F.col("btc_price_json"), ConsumerBTCPrice))\
    .select("parsed_json.*")
btc_price_max_per_minute = btc_price_df\
    .withWatermark("last_updated", "1 minute")\
    .groupby(F.window("last_updated", "30 seconds", "30 seconds"))\
    .agg(F.max(F.col("btc_price_usd")).alias("max_btc_price_usd"))

raw_data_target_path = "s3a://btc-price-kafka-project/btc_price_raw"
agg_data_target_path = "s3a://btc-price-kafka-project/btc_price_per_minute"
raw_checkpoint_path = "s3a://btc-price-kafka-project/checkpoints/btc_price_raw"
agg_checkpoint_path = "s3a://btc-price-kafka-project/checkpoints/btc_price_data"

write_raw_query = btc_price_df.writeStream.format("parquet")\
    .option("path", raw_data_target_path)\
    .option("checkpointLocation", raw_checkpoint_path)\
    .outputMode("append")\
    .start()
write_agg_query = btc_price_max_per_minute.writeStream.format("parquet") \
    .option("path", agg_data_target_path)\
    .option("checkpointLocation", agg_checkpoint_path)\
    .outputMode("append")\
    .start()
spark.streams.awaitAnyTermination()
