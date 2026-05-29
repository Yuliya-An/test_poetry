"""Модуль для конвертации валют с использованием внешнего API."""

from requests.exceptions import RequestException


import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CURRENCY_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rubles(amount: float, currency: str) -> Optional[float]:
    """
    Конвертирует сумму из указанной валюты в рубли.
    """
    if not API_KEY:
        return None

    headers = {"apikey": API_KEY}
    params = {"base": currency, "symbols": "RUB"}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        rate = data.get("rates", {}).get("RUB")
        if rate is None:
            return None
        return amount * float(rate)

    except RequestException:
        return None
    except (KeyError, TypeError, ValueError):
        return None
