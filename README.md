# Виджет банковских операций
## Описание:

Проект "Виджет банковских операций" - это веб-приложение на Python для работы с банковскими данными пользователей и корректным отражением их в приложении с помощью масок и сортировки.

## Установка:

1. Клонируйте репозиторий:
```
git clone git@github.com:ksucha1894-gif/dz_project.git
```
2. Установите Python в случае его отсутствия.

## Использование:

1. Введите свои данные банковского счета или карты и воспользуйтесь функцией def mask_account_card или def get_date

Пример:
Входные данные:
Visa Platinum 7000792289606361

def mask_account_card(number: str, account_number: str) -> str:
    """
       Функция принимает тип и число - тип и номер карты, тип и номер расчетного счета
       Маска преобразует тип и число в формат тип XXXX XX** **** XXXX или в **XXXX
       """
    card_info, number = number.rsplit(' ', maxsplit=1)
    if 'счет' in card_info.lower():
        masked_number = get_mask_card_number(number)
    else:
        masked_number = get_mask_account(account_number)

    return f'{card_info} {masked_number}'

Выход функции с маской:
Visa Platinum 7000 79** **** 6361


2. Введите свои данные или дату и воспользуйтесь функцией def filter_by_state или def sort_by_date

Пример:
Входные данные функции:
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

def filter_by_state(banking_operations: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    Возвращает новый список словарей, содержащий только те словари, у которых значение ключа 'state' соответствует
    указанному.
    """
    return [operation for operation in banking_operations if operation.get('state') == state]

Выход функции со статусом по умолчанию 'EXECUTED':
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
