import pytest
from unittest.mock import patch, Mock
from src.external_api import convert_transaction_to_rubles


def test_rub_transaction_returns_amount():
    tx = {"amount": 100, "currency": "RUB"}
    assert convert_transaction_to_rubles(tx) == 100.0


def test_other_currency_returns_amount():
    tx = {"amount": 50, "currency": "GBP"}
    assert convert_transaction_to_rubles(tx) == 50.0


@patch("src.external_api.requests.get")
def test_usd_conversion_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 75.0}}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    tx = {"amount": 10, "currency": "USD"}
    result = convert_transaction_to_rubles(tx)
    assert result == 750.0


@patch("src.external_api.requests.get")
def test_api_failure_returns_none(mock_get):
    mock_get.side_effect = Exception("API failure")

    tx = {"amount": 10, "currency": "USD"}
    result = convert_transaction_to_rubles(tx)
    assert result is None


def test_missing_amount_or_currency():
    assert convert_transaction_to_rubles({"amount": 10}) is None
    assert convert_transaction_to_rubles({"currency": "USD"}) is None
