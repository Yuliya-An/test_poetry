import logging

logger = logging.getLogger(__name__)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, показывая только первые 6 и последние 4 цифры.
    Остальные цифры заменяются звездочками и форматируются в виде XXXX XX** **** XXXX.
    """
    logger.debug(f"Начинаем маскировку карты: {card_number[:10]}...")

    try:
        digits = card_number.replace(" ", "")
        if len(digits) < 16:
            logger.error(f"Недостаточно цифр в номере карты: {card_number}")
            raise ValueError("Количество цифр в номере карты должно быть не менее 16")

        first_digits = digits[:6]
        last_digits = digits[-4:]

        masked = f"{first_digits[:4]} {first_digits[4:6]}** **** {last_digits}"
        logger.info(f"Номер карты успешно преобразован: {masked}")
        return masked

    except Exception as e:
        logger.error(f"Сбой при обработке карты: {e}", exc_info=True)
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, показывая только последние 4 цифры.
    Перед ними две звездочки.
    """
    logger.debug(f"Обрабатываем номер счёта: {account_number[:10]}...")

    try:
        digits = account_number.replace(" ", "")

        if len(digits) < 4:
            logger.error(f"Слишком короткий номер счёта: {account_number}")
            raise ValueError("Длина номера счета должна быть не менее 4 цифр")

        last_four = digits[-4:]
        masked = f"**{last_four}"
        logger.info(f"Счёт замаскирован: {masked}")
        return masked

    except Exception as e:
        logger.error(f"Проблема при маскировании счёта: {e}", exc_info=True)
        raise


# # Запрос номера карты у пользователя
# card_input = input("Введите номер карты: ")
#
# # Запрос номера счета у пользователя
# account_input = input("Введите номер счета: ")
#
# # Маскируем номера
# masked_card = get_mask_card_number(card_input)
# masked_account = get_mask_account(account_input)
#
# # Выводим результат
# print("Маскированный номер карты:", masked_card)
# print("Маскированный номер счета:", masked_account)
