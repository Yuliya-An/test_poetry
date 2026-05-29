"""
Модуль для чтения финансовых операций из CSV, XLSX и JSON файлов.
"""
import logging
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Union

logger = logging.getLogger(__name__)


def read_json_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла и возвращает список словарей.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Неверное расширение файла или некорректный формат JSON.
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"JSON файл не найден: {file_path}")
        raise FileNotFoundError(f"Файл {file_path} не существует.")
    if path.suffix.lower() != '.json':
        raise ValueError(f"Ожидается .json файл, получен {path.suffix}")
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON файл должен содержать список транзакций")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON {file_path}: {e}")
        raise ValueError(f"Некорректный формат JSON в файле {file_path}") from e


def read_csv_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает транзакции из CSV-файла и возвращает список словарей.

    Args:
        file_path: Путь к CSV-файлу (например, "data/transactions.csv").

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Неверное расширение файла.
        pd.errors.EmptyDataError: Файл пуст.
    """
    path = Path(file_path)

    # Проверяем существование файла
    if not path.exists():
        logger.error(f"CSV файл не найден: {file_path}")
        raise FileNotFoundError(f"Файл {file_path} не существует.")

    # Проверяем расширение
    if path.suffix.lower() != '.csv':
        raise ValueError(f"Ожидается .csv файл, получен {path.suffix}")

    try:
        df = pd.read_csv(path, encoding='utf-8', sep=';')  # <-- вот тут добавил sep=';'
        if df.empty:
            logger.warning(f"CSV файл пуст: {file_path}")
            return []

        transactions = df.to_dict('records')
        logger.info(f"Загружено {len(transactions)} транзакций из {file_path}")
        return transactions   # type: ignore[return-value]

    except pd.errors.EmptyDataError:
        logger.warning(f"CSV файл пуст: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка чтения CSV {file_path}: {e}")
        raise


def read_excel_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает транзакции из Excel-файла (XLSX) и возвращает список словарей.

    Args:
        file_path: Путь к XLSX-файлу (например, "data/transactions_excel.xlsx").

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Неверное расширение файла.
    """
    path = Path(file_path)

    # Проверяем существование файла
    if not path.exists():
        logger.error(f"Excel файл не найден: {file_path}")
        raise FileNotFoundError(f"Файл {file_path} не существует.")

    # Проверяем расширение
    if path.suffix.lower() not in ['.xlsx', '.xls']:
        raise ValueError(f"Ожидается .xlsx или .xls файл, получен {path.suffix}")

    try:
        df = pd.read_excel(path, engine='openpyxl')
        if df.empty:
            logger.warning(f"Excel файл пуст: {file_path}")
            return []

        transactions = df.to_dict('records')
        logger.info(f"Загружено {len(transactions)} транзакций из {file_path}")
        return transactions   # type: ignore[return-value]

    except Exception as e:
        logger.error(f"Ошибка чтения Excel {file_path}: {e}")
        raise


def get_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Универсальная функция для чтения транзакций по расширению файла.

    Args:
        file_path: Путь к файлу (.csv, .xlsx, .xls или .json).

    Returns:
        Список транзакций.

    Raises:
        ValueError: Неподдерживаемое расширение файла.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == '.csv':
        return read_csv_transactions(path)
    elif suffix in ['.xlsx', '.xls']:
        return read_excel_transactions(path)
    elif suffix == '.json':
        return read_json_transactions(path)
    else:
        raise ValueError(
            f"Неподдерживаемый формат файла: {suffix}. "
            f"Поддерживаемые форматы: .csv, .xlsx, .xls, .json"
        )
