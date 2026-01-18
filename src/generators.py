from typing import Any, Iterator, List, Dict


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному коду валюты.
    Возвращает итератор по транзакциям с нужной валютой.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который поочерёдно возвращает описание каждой транзакции.
    Если описание отсутствует, возвращает строку "Описание отсутствует".
    """
    for transaction in transactions:
        description = transaction.get("description", "Описание отсутствует")
        yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    Генерирует номера от start до stop включительно.
    """
    for number in range(start, stop + 1):
        card_str = f"{number:016d}"  # Форматируем число с ведущими нулями до 16 цифр
        formatted = " ".join(card_str[i : i + 4] for i in range(0, 16, 4))
        yield formatted
