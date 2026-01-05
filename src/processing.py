from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует банковские операции по статусу (по умолчанию EXECUTED)."""
    result = []
    for transaction in transactions:
        if transaction.get("state") == state:
            result.append(transaction)
    return result


def sort_by_date(transactions: List[Dict[str, Any]], reverse_sort: bool = True) -> List[Dict[str, Any]]:
    """Сортирует банковские операции по дате (по умолчанию новые сверху)."""
    return sorted(transactions, key=lambda t: t["date"], reverse=reverse_sort)


# Тесты (закомментировать перед сдачей)
if __name__ == "__main__":
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("EXECUTED:", filter_by_state(data))
    print("CANCELED:", filter_by_state(data, "CANCELED"))
    print("СОРТИРОВКА:", sort_by_date(data))
