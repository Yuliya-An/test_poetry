def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, показывая только первые 6 и последние 4 цифры.
    Остальные цифры заменяются звездочками и форматируются в виде XXXX XX** **** XXXX.
    """
    digits = card_number.replace(" ", "")
    if len(digits) < 16:
        raise ValueError("Количество цифр в номере карты должно быть не менее 16")

    first_digits = digits[:6]
    last_digits = digits[-4:]

    return f"{first_digits[:4]} {first_digits[4:6]}** **** {last_digits}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, показывая только последние 4 цифры.
    Перед ними две звездочки.
    """
    digits = account_number.replace(" ", "")

    if len(digits) < 4:
        raise ValueError("Длина номера счета должна быть не менее 4 цифр")
    last_four = digits[-4:]
    return f"**{last_four}"


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
