"""Модуль для чтения операций из JSON-файла."""
import json
from typing import Any


def read_operations_from_json(filepath: str) -> list[dict[str, Any]]:
    """
    Загружает список банковских операций из JSON-файла.

    Args:
        filepath: Путь к JSON-файлу с операциями.

    Returns:
        Список словарей с операциями. Если файл не найден или некорректен — пустой список.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data: Any = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []
