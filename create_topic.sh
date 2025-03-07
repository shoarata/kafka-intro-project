#!/bin/bash
docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic system-logs --bootstrap-server kafka:9092
