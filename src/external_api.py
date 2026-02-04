import os
from typing import Optional, Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CURRENCY_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/live"


def convert_transaction_to_rubles(transaction: dict[str, Any]) -> Optional[float]:
    """
    Принимает транзакцию (dict) с ключами 'amount' и 'currency'.
    Если валюта USD или EUR — конвертирует сумму в RUB через API.
    Иначе возвращает сумму как float.
    """
    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if amount is None or currency is None:
        return None

    if currency == "RUB":
        return float(amount)

    if currency not in ("USD", "EUR"):
        # Для других валют пока не конвертируем
        return float(amount)

    if not API_KEY:
        raise RuntimeError("API key not found in environment variables")

    headers = {"apikey": API_KEY}
    params = {
        "base": currency,
        "symbols": "RUB"
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        rate = data.get("rates", {}).get("RUB")
        if rate is None:
            return None
        return float(amount) * float(rate)
    except (requests.RequestException, Exception):
        return None
