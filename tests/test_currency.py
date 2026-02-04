import pytest
from unittest.mock import patch, Mock
from src.utils.currency import convert_to_rubles


def test_convert_to_rubles_no_api_key():
    """Проверяем, что без API-ключа функция возвращает None."""
    with patch.dict('os.environ', {}, clear=True):
        result = convert_to_rubles(100, 'USD')
        assert result is None


def test_convert_to_rubles_with_valid_response():
    """Проверяем успешную конвертацию с моком API."""
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_response.raise_for_status = Mock()

    with patch.dict('os.environ', {'CURRENCY_API_KEY': 'test_key'}), \
         patch('requests.get', return_value=mock_response):
        result = convert_to_rubles(100, 'USD')
        assert result == 9050.0  # 100 * 90.5


def test_convert_to_rubles_api_error():
    """Проверяем обработку ошибки запроса."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception('API error')

    with patch.dict('os.environ', {'CURRENCY_API_KEY': 'test_key'}), \
         patch('requests.get', return_value=mock_response):
        result = convert_to_rubles(100, 'USD')
        assert result is None


def test_convert_to_rubles_invalid_currency():
    """Проверяем случай, когда API не возвращает курс для валюты."""
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"EUR": 0.9}}  # Нет RUB
    mock_response.raise_for_status = Mock()

    with patch.dict('os.environ', {'CURRENCY_API_KEY': 'test_key'}), \
         patch('requests.get', return_value=mock_response):
        result = convert_to_rubles(100, 'JPY')
        assert result is None
