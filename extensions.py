import requests
from config import *
import json

class APIException(Exception):
    pass


class API:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(
                f'Нельзя конвертировать одинаковые валюты {base}.\nВведите команды заново.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не смог обработать валюту {quote}.\nВведите команды заново.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не смог обработать валюту {base}.\nВведите команды заново.')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Не смог обработать количество {amount}.\nВведите команды заново.')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[keys[quote]])
        return total_base*amount
