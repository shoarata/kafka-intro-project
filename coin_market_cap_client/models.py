from typing import List
from pydantic import BaseModel
import datetime

from coin_market_cap_client.currency_symbols import Currency


class ConversionQuote(BaseModel):
    symbol: Currency
    price: float
    last_updated: datetime.datetime

class CurrencyConversion(BaseModel):
    symbol: Currency
    id: int
    name: str
    amount: float
    last_updated: datetime.datetime
    quotes: List[ConversionQuote]