import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует банковские операции по статусу."""
    target_state = state.upper()
    return [
        t for t in transactions
        if str(t.get("state", "")).upper() == target_state
    ]


def sort_by_date(transactions: List[Dict[str, Any]], reverse_sort: bool = True) -> List[Dict[str, Any]]:
    """Сортирует банковские операции по дате."""
    return sorted(transactions, key=lambda t: t["date"], reverse=reverse_sort)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Поиск операций по строке в описании."""
    return [item for item in data if re.search(search, item.get('description', ''), re.IGNORECASE)]


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчет количества операций по категориям."""
    descriptions = [item.get('description', '') for item in data]
    counts = Counter(descriptions)
    return {category: counts[category] for category in categories}


def mask_account_number(account: str) -> str:
    """Маскирует номер счета, оставляя последние 4 символа."""
    if not isinstance(account, str):
        return ""
    visible_digits = 4
    masked_part = "*" * max(len(account) - visible_digits, 0)
    return masked_part + account[-visible_digits:]


def extract_amount(transaction: dict) -> str:
    """Извлекает сумму и валюту операции из разных форматов."""
    amount = transaction.get("amount")
    if isinstance(amount, dict):
        value = amount.get("value", "")
        currency = amount.get("currency", "")
        if value:
            return f"{value} {currency}".strip()
    if amount is not None:
        currency = transaction.get("currency_code", "") or transaction.get("currency", "")
        return f"{amount} {currency}".strip()
    alt_amount = transaction.get("operationAmount") or transaction.get("sum")
    if isinstance(alt_amount, dict):
        value = alt_amount.get("value", "")
        currency = alt_amount.get("currency", "")
        if value:
            return f"{value} {currency}".strip()
    elif alt_amount:
        currency = transaction.get("currency_code", "") or transaction.get("currency", "")
        return f"{alt_amount} {currency}".strip()
    return "нет суммы"


def filter_by_currency(transactions: List[dict], currency: str) -> List[dict]:
    """Фильтрует транзакции по коду валюты."""
    currency_upper = currency.upper()
    result = []
    for tr in transactions:
        code = tr.get("currency_code", "")
        if str(code).upper() == currency_upper:
            result.append(tr)
            continue
        amount = tr.get("amount")
        if isinstance(amount, dict):
            curr = amount.get("currency", "")
            if str(curr).upper() == currency_upper:
                result.append(tr)
                continue
    return result
