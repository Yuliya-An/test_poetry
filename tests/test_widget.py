import pytest
from unittest.mock import patch, MagicMock
from src.widget import get_date, mask_account_card, get_last_operations


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("", ""),
        ("Некорректная карта 123", "Некорректная карта 123"),
        ("Карта 123456789012345", "Карта 123456789012345"),
    ],
)
def test_mask_account_card(text: str, expected: str) -> None:
    assert mask_account_card(text) == expected


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("", ""),
    ],
)
def test_get_date(date_str: str, expected: str) -> None:
    assert get_date(date_str) == expected


@patch("src.widget.read_operations_from_json")
@patch("src.widget.convert_to_rubles")
def test_get_last_operations_success(mock_convert: MagicMock, mock_read: MagicMock) -> None:
    mock_read.return_value = [
        {
            "state": "EXECUTED",
            "date": "2024-01-01T10:00:00",
            "description": "Перевод",
            "from": "Счет 1234567890",
            "to": "Карта 1111222233334444",
            "operationAmount": {"amount": "100", "currency": {"code": "USD"}},
        },
        {
            "state": "CANCELED",
            "date": "2024-01-02T10:00:00",
            "operationAmount": {"amount": "50", "currency": {"code": "RUB"}},
        },
    ]
    mock_convert.return_value = 7500.0

    result = get_last_operations()

    assert len(result) == 1
    assert result[0]["amount"] == 7500.0
    assert result[0]["currency"] == "RUB"
    assert "Счет **7890" in result[0]["from"]
