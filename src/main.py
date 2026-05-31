from typing import List
from processing import (
    filter_by_state, sort_by_date, process_bank_search,
    filter_by_currency, extract_amount
)
from csv_excel_loader import get_transactions
from widget import mask_account_card  # Импортируем маскировку из виджета


def format_date(date_str: str) -> str:
    """Преобразует дату из ISO формата в ДД.ММ.ГГГГ"""
    if not date_str or len(date_str) < 10:
        return "нет даты"
    return f"{date_str[8:10]}.{date_str[5:7]}.{date_str[:4]}"


def input_with_options(prompt: str, options: List[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice.upper() in [opt.upper() for opt in options]:
            return choice.upper()
        print(f'Статус операции "{choice}" недоступен.')
        print(f'Доступные для фильтрации статусы: {", ".join(options)}')


def yes_no_prompt(prompt: str) -> bool:
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['да', 'д', 'yes', 'y']:
            return True
        elif choice in ['нет', 'н', 'no', 'n']:
            return False
        print('Пожалуйста, введите "Да" или "Нет".')


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию из JSON-файла")
    print("2. Получить информацию из CSV-файла")
    print("3. Получить информацию из XLSX-файла")

    file_choice = input_with_options("Ваш выбор: ", ['1', '2', '3'])
    file_paths = {
        '1': 'data/operations.json',
        '2': 'data/transactions.csv',
        '3': 'data/transactions_excel.xlsx'
    }
    selected_file = file_paths[file_choice]
    print(f"Для обработки выбран файл: {selected_file}")

    try:
        transactions = get_transactions(selected_file)
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    status = input_with_options(
        f"Введите статус для фильтрации.\nДоступные статусы: {', '.join(statuses)}\n", statuses
    )
    filtered_transactions = filter_by_state(transactions, status)

    if not filtered_transactions:
        print("Транзакции с таким статусом не найдены.")
        return

    if yes_no_prompt("Программа: Выводить только рублевые транзакции? Да/Нет: "):
        filtered_transactions = filter_by_currency(filtered_transactions, 'RUB')
        if not filtered_transactions:
            print("Рублевые транзакции не найдены.")
            return

    if yes_no_prompt("Хотите отсортировать транзакции по дате? (Да/Нет): "):
        ascending = yes_no_prompt("Сортировать по возрастанию? (Да/Нет): ")
        filtered_transactions = sort_by_date(filtered_transactions, reverse_sort=not ascending)

    if yes_no_prompt("Фильтровать транзакции по ключевому слову в описании? (Да/Нет): "):
        keyword = input("Введите ключевое слово для поиска: ").strip()
        filtered_transactions = process_bank_search(filtered_transactions, keyword)

        if not filtered_transactions:
            print("По вашему запросу транзакции не найдены.")
            return

    print(f"\nВсего транзакций: {len(filtered_transactions)}\n")

    for t in filtered_transactions:
        date = format_date(t.get('date', 'нет даты'))
        description = t.get('description', 'нет описания')

        # Маскировка счетов через виджет
        from_account = mask_account_card(t.get('from', ''))
        to_account = mask_account_card(t.get('to', ''))

        # ВНИМАНИЕ: Используем нашу универсальную функцию для суммы
        # Она сама разберется, словарь там или число, и добавит "руб."
        amount_str = extract_amount(t)

        print(f"{date} {description}")
        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif from_account:
            print(from_account)
        elif to_account:
            print(to_account)

        print(f"Сумма: {amount_str}\n")


if __name__ == "__main__":
    main()
