from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(user_card: str) -> str:
    """Функция маскирует номер карты или счета"""
    if len(user_card) <= 0:
        raise ValueError("Ошибка ввода! Пожалуйста, введите номер карты или счета.")
    elif "Счет" in user_card:
        mask_ac_num = f"{user_card[:4]} {get_mask_account(user_card[5:])}"
        return mask_ac_num
    else:
        mask_card_num = f"{user_card[:-16]}{get_mask_card_number(user_card[-16:])}"
        return mask_card_num


def get_date(user_date: str) -> str:
    """Функция корректирует дату в формат ДД.ММ.ГГГГ"""
    return f"{user_date[8:10]}.{user_date[5:7]}.{user_date[:4]}"


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
