import pytest
import json
from unittest.mock import patch, mock_open
from src.utils.file_reader import read_operations_from_json  # Проверь путь к файлу!


def test_read_json_success() -> None:
    """Тест успешного чтения списка операций."""
    mock_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    mock_content = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = read_operations_from_json("dummy.json")
        assert result == mock_data


def test_read_json_file_not_found() -> None:
    """Тест ошибки: файл не найден."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_operations_from_json("missing.json")


def test_read_json_decode_error() -> None:
    """Тест ошибки: невалидный JSON."""
    mock_content = "это не json, а просто текст"

    with patch("builtins.open", mock_open(read_data=mock_content)):
        with pytest.raises(json.JSONDecodeError):
            read_operations_from_json("bad_format.json")


def test_read_json_not_a_list() -> None:
    """Тест ошибки: JSON валиден, но это не список (например, словарь)."""
    mock_data = {"key": "value"}  # Это словарь, а не список!
    mock_content = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_content)):
        with pytest.raises(ValueError, match="Ожидался список операций"):
            read_operations_from_json("not_a_list.json")
