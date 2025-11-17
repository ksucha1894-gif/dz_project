from datetime import datetime
from typing import Union


def filter_by_state(banking_operations: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    Возвращает новый список словарей, содержащий только те словари, у которых значение ключа 'state' соответствует
    указанному.
    """
    return [operation for operation in banking_operations if operation.get('state') == state]


def sort_by_date(
    date_operations: list[dict[str, Union[str, datetime]]],
    state: str = 'EXECUTED',
    key: str = "desc"
) -> list[dict[str, Union[str, datetime]]]:
    """
    Фильтрует и сортирует список словарей по полю 'date'.
    Возвращает новый список словарей, содержащий только те словари, у которых значение ключа 'state' соответствует
    указанному, отсортированный по дате.
    """
    filtered_operations = [op for op in date_operations if op['state'] == state]
    reverse_sort = True if key == "desc" else False
    return sorted(
        filtered_operations,
        key=lambda x: datetime.strptime(str(x['date']), '%Y-%m-%dT%H:%M:%S.%f'),
        reverse=reverse_sort
    )
