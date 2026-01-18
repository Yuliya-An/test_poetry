import pytest
from typing import List, Dict, Any

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 1"},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}, "description": "Payment 2"},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 3"},
    ]


def test_filter_by_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions == ["Payment 1", "Payment 2", "Payment 3"]


def test_card_number_generator() -> None:
    gen = card_number_generator(1, 3)
    expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert list(gen) == expected
