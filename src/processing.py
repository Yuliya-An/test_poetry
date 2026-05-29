import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует банковские операции по статусу (с приведением к единому регистру)."""
    target_state = state.upper()
    # Используем list comprehension для скорости и чистоты кода
    # Приводим значение к строке, чтобы избежать ошибок с NaN/float из Excel
    return [
        t for t in transactions
        if str(t.get("state", "")).upper() == target_state
    ]


def sort_by_date(transactions: List[Dict[str, Any]], reverse_sort: bool = True) -> List[Dict[str, Any]]:
    """Сортирует банковские операции по дате."""
    return sorted(transactions, key=lambda t: t["date"], reverse=reverse_sort)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Поиск операций по заданной строке-шаблону в описании с использованием re."""
    # Ищем в поле 'description', игнорируя регистр
    return [item for item in data if re.search(search, item.get('description', ''), re.IGNORECASE)]


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчет количества операций по категориям из поля description с помощью Counter."""
    descriptions = [item.get('description', '') for item in data]
    counts = Counter(descriptions)
    # Возвращаем только те категории, которые были переданы в списке categories
    return {category: counts[category] for category in categories}


def mask_account_number(account: str) -> str:
    """
    Маскирует номер счета/карты, оставляя последние 4 символа открытыми.
    Например, "1234567890123456" -> "************3456"
    """
    if not isinstance(account, str):
        return ""
    visible_digits = 4
    masked_part = "*" * max(len(account) - visible_digits, 0)
    return masked_part + account[-visible_digits:]


def extract_amount(transaction: dict) -> str:
    """
    Извлекает сумму операции из разных форматов.
    Для JSON это может быть {'amount': {'value': '100.00', 'currency': 'USD'}}
    Для CSV/Excel — просто число или строка.
    """
    amount = transaction.get("amount")
    if isinstance(amount, dict):
        value = amount.get("value", "")
        currency = amount.get("currency", "")
        return f"{value} {currency}".strip()
    elif amount:
        return str(amount)
    # Если ключа amount нет, попробуем другие варианты
    # Например, в JSON могут быть поля 'operationAmount' или 'sum'
    alt_amount = transaction.get("operationAmount") or transaction.get("sum")
    if isinstance(alt_amount, dict):
        value = alt_amount.get("value", "")
        currency = alt_amount.get("currency", "")
        return f"{value} {currency}".strip()
    elif alt_amount:
        return str(alt_amount)
    return "нет суммы"


def filter_by_currency(transactions: List[dict], currency: str) -> List[dict]:
    """
    Фильтрует список транзакций по коду валюты из колонки currency_code.
    """
    currency_upper = currency.upper()
    # Ищем напрямую в ключе 'currency_code', который мы видели в твоей таблице
    return [
        tr for tr in transactions
        if str(tr.get("currency_code", "")).upper() == currency_upper
    ]
