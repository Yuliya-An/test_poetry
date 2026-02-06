from typing import List, Dict, Any
from .utils.currency import convert_to_rubles
from .utils.file_reader import read_operations_from_json


def mask_account_card(user_card: str) -> str:
    """Функция маскирует номер карты или счета"""
    if not user_card:
        return ""
    if "Счет" in user_card:
        return f"Счет **{user_card[-4:]}"
    # Если это карта
    parts = user_card.split()
    number = parts[-1]
    name = " ".join(parts[:-1])
    if len(number) == 16 and number.isdigit():
        return f"{name} {number[:4]} {number[4:6]}** **** {number[-4:]}"
    return user_card


def get_date(user_date: str) -> str:
    """Функция корректирует дату в формат ДД.ММ.ГГГГ"""
    if not user_date:
        return ""
    # user_date имеет формат "2024-01-15T12:30:00.000Z"
    return f"{user_date[8:10]}.{user_date[5:7]}.{user_date[:4]}"


def get_last_operations(file_path: str = "data/operations.json", count: int = 5) -> List[Dict[str, Any]]:
    """Возвращает последние count выполненных операций."""
    # Читаем данные из файла
    operations = read_operations_from_json(file_path)
    if not operations:
        return []

    # Фильтруем только выполненные операции
    executed_ops = [op for op in operations if isinstance(op, dict) and op.get("state") == "EXECUTED"]

    # Сортируем по дате (самые новые первые)
    executed_ops.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Берем нужное количество
    last_ops = executed_ops[:count]

    # Обрабатываем каждую операцию
    result: List[Dict[str, Any]] = []
    for op in last_ops:
        # Получаем сумму и валюту
        operation_amount = op.get("operationAmount", {})
        amount = operation_amount.get("amount")
        currency = operation_amount.get("currency", {}).get("code")

        # Конвертируем сумму в рубли
        amount_rub = None
        if amount and currency:
            if currency != "RUB":
                try:
                    amount_rub = convert_to_rubles(float(amount), currency)
                except Exception:
                    # Если конвертация не удалась, оставляем исходную сумму
                    amount_rub = float(amount)
            else:
                amount_rub = float(amount)

        # Маскируем номера счетов/карт
        description = op.get("description", "")
        from_account = mask_account_card(op.get("from", "")) if op.get("from") else ""
        to_account = mask_account_card(op.get("to", "")) if op.get("to") else ""
        # Форматируем дату
        date_str = get_date(op.get("date", ""))

        # Собираем результат
        processed_op = {
            "date": date_str,
            "description": description,
            "from": from_account,
            "to": to_account,
            "amount": amount_rub if amount_rub is not None else amount,
            "currency": "RUB" if amount_rub is not None else currency,
        }
        result.append(processed_op)
    return result


# # Запрос номера карты у пользователя
# card_input = input("Введите номер карты: ")
#
# # Запрос номера счета у пользователя
# account_input = input("Введите номер счета: ")
#
# # Ввод даты в формате ISO
# date_input = input("Введите дату в формате ГГГГ-ММ-ДДТЧ:ММ:СС.микросекунды: ")
#
# # Маскируем номера
# masked_card = get_mask_card_number(card_input)
# masked_account = get_mask_account(account_input)
#
# # Форматируем дату
# formatted_date = get_date(date_input)
#
#
# # Выводим результаты
# print("Маскированная карта:", masked_card)
# print("Маскированный счет:", masked_account)
# print("Форматированная дата:", formatted_date)
