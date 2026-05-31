from typing import List, Dict, Any
from src.utils.currency import convert_to_rubles
from src.utils.file_reader import read_operations_from_json


def mask_account_card(user_card) -> str:
    """Функция маскирует номер карты или счета с безопасной обработкой"""
    if not user_card:
        return ""

    # Преобразуем в строку, если это не строка
    user_card_str = str(user_card)

    if "Счет" in user_card_str:
        return f"Счет **{user_card_str[-4:]}"

    parts = user_card_str.split()
    if len(parts) < 2:
        return user_card_str

    name = " ".join(parts[:-1])
    number = parts[-1]

    if len(number) == 16 and number.isdigit():
        return f"{name} {number[:4]} {number[4:6]}** **** {number[-4:]}"

    return user_card_str


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
        # Проверяем, что amount и currency существуют и не являются словарями
        clean_amount = amount.get('amount') if isinstance(amount, dict) else amount
        clean_currency = currency.get('code') if isinstance(currency, dict) else currency

        if clean_amount and clean_currency:
            try:
                if clean_currency != "RUB":
                    amount_rub = convert_to_rubles(float(clean_amount), clean_currency)
                else:
                    amount_rub = float(clean_amount)
            except Exception:
                amount_rub = float(clean_amount) if clean_amount else None

        # Формируем финальную строку суммы с валютой (то, что хочет Александра)
        if amount_rub is not None:
            final_amount_str = f"{amount_rub} руб."
        elif clean_amount:
            # Если конвертация не сработала, но сумма есть — добавляем руб. по умолчанию
            final_amount_str = f"{clean_amount} руб."
        else:
            final_amount_str = "0.0 руб."

        # Маскируем номера счетов/карт
        description = op.get("description", "")
        from_account = mask_account_card(op.get("from", "")) if op.get("from") else ""
        to_account = mask_account_card(op.get("to", "")) if op.get("to") else ""
        date_str = get_date(op.get("date", ""))

        # Собираем результат
        processed_op = {
            "date": date_str,
            "description": description,
            "from": from_account,
            "to": to_account,
            "amount": final_amount_str,  # Теперь здесь сразу красивая строка!
        }
        result.append(processed_op)
    return result
