import datetime

from pydantic import BaseModel
from pyspark.sql.types import StructType, StructField, DoubleType, TimestampType


class ProducerBTCPrice(BaseModel):
    last_updated: datetime.datetime
    btc_price_usd: float

ConsumerBTCPrice = StructType([
    StructField("last_updated", TimestampType()),
    StructField("btc_price_usd", DoubleType())
])