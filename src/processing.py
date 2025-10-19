from datetime import datetime


def filter_by_state(banking_operations: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    Возвращает новый список словарей, содержащий только те словари, у которых значение ключа 'state' соответствует
    указанному.
    """
    return [operation for operation in banking_operations if operation.get('state') == state]


def sort_by_date(
    date_operations: list[dict[str, Union[str, datetime]]],
    key: str = "desc"
) -> list[dict[str, Union[str, datetime]]]:
    """
    Сортирует список словарей по полю 'date'.
    Возвращает новый список словарей, отсортированный по дате.
    """
    reverse_sort = True if key == "desc" else False
    return sorted(
        data_banking_operations,
        key=lambda x: datetime.strptime(x['date'] if isinstance(x['date'], str)
                                        else x['date'].isoformat(), '%Y-%m-%d'),
        reverse=reverse_sort
    )
