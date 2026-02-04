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


@pytest.mark.parametrize(
    "currency_code, expected_count",
    [
        ("USD", 2),
        ("EUR", 1),
        ("RUB", 0),
    ],
)
def test_filter_by_currency(
    sample_transactions: List[Dict[str, Any]],
    currency_code: str,
    expected_count: int,
) -> None:
    filtered = list(filter_by_currency(sample_transactions, currency_code))
    assert len(filtered) == expected_count
    if expected_count > 0:
        assert all(
            t["operationAmount"]["currency"]["code"] == currency_code
            for t in filtered
        )


def test_filter_by_currency_empty_list() -> None:
    result = list(filter_by_currency([], "USD"))
    assert len(result) == 0


@pytest.mark.parametrize(
    "index, expected_description",
    [
        (0, "Payment 1"),
        (1, "Payment 2"),
        (2, "Payment 3"),
    ],
)
def test_transaction_descriptions(
    sample_transactions: List[Dict[str, Any]],
    index: int,
    expected_description: str,
) -> None:
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions[index] == expected_description


def test_transaction_descriptions_empty_list() -> None:
    result = list(transaction_descriptions([]))
    assert len(result) == 0


@pytest.mark.parametrize(
    "start, stop, expected_results",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (
            9999999999999998,
            9999999999999999,
            ["9999 9999 9999 9998", "9999 9999 9999 9999"],
        ),
        (
            1000,
            1002,
            ["0000 0000 0000 1000", "0000 0000 0000 1001", "0000 0000 0000 1002"],
        ),
    ],
)
def test_card_number_generator(
    start: int,
    stop: int,
    expected_results: List[str],
) -> None:
    gen = card_number_generator(start, stop)
    assert list(gen) == expected_results
