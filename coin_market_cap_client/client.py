import json

import requests
from typing import List

from coin_market_cap_client import envs, host_urls
from coin_market_cap_client.currency_symbols import Currency
from coin_market_cap_client.errors import ServiceError
from coin_market_cap_client.models import CurrencyConversion, ConversionQuote


class CoinMarketCapClient:
    def __init__(self, api_key: str, env: str=envs.DEV):
        assert env in (envs.DEV, envs.PROD)
        if env == envs.DEV:
            self.host_url = host_urls.dev_host
        else:
            self.host_url = host_urls.prod_host
        self.session  = requests.session()
        self.session.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key
        })


    def get_latest_price(self, from_symbol: Currency, to_symbols: List[Currency]) -> CurrencyConversion:
       url = f"{self.host_url}/v2/tools/price-conversion"
       parameters = {
           "amount": 1,
           "symbol": from_symbol.value,
           "convert": ",".join([cur.value for cur in to_symbols])
       }
       try:
           response = self.session.get(url=url, params=parameters)
           if response.ok:
               resp_data = response.json()["data"][0]
               return CurrencyConversion(
                   symbol=resp_data["symbol"],
                   id=resp_data["id"],
                   name=resp_data["name"],
                   amount=resp_data["amount"],
                   last_updated=resp_data["last_updated"],
                   quotes=CoinMarketCapClient._extract_quotes(resp_data["quote"])
               )
           else:
               raise ServiceError(f"Error: {response.json()['status']}")

       except requests.ConnectionError as e:
           raise ServiceError(f"Connection error {e}")


    @staticmethod
    def _extract_quotes(response_quotes: dict) -> List[ConversionQuote]:
        quotes = []
        for currency_symbol, price_dct in response_quotes.items():
            quotes.append(
                ConversionQuote(symbol=currency_symbol, price=price_dct["price"], last_updated=price_dct["last_updated"])
            )
        return quotes






