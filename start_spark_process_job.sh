#!/bin/bash

spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-spark_2.12:3.3.0 \
spark_stream_process_btc_price.py