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

3. Проведены тесты на разные виды данных и дат:
@pytest.mark.parametrize("number, masked_number", [
    ("7000792289606361", "7000 79** **** 6361"),
    ("123456781234", "1234 56** **** 1234"),
    ("56789012345432134", "5678 90** **** 2134"),
    ("0000000000000000", "0000 00** **** 0000"),
    ("", " ** **** ")
])
def test_get_mask_card_number(number: str, masked_number: str) -> None:
    assert get_mask_card_number(number) == masked_number


@pytest.mark.parametrize("number, account_number", [
    ("73654108430135874305", "**4305"),
    ("DE89370400440532013000", "**3000"),
    ("KZ75 125K ZT10 0130 0335", "**0335"),
    ("12345678912345", "**2345"),
    ("", "**")
])
def test_get_mask_account(number: str, account_number: str) -> None:
    assert get_mask_account(number) == account_number


@pytest.mark.parametrize("number, expected_mask", [
    ("Карта 7000792289606361", "Карта 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("", "")
])
def test_mask_account_card(number: str, expected_mask: str) -> None:
    # Не вызываем split, если строка пустая или состоит только из пробелов
    if number.strip():
        assert (mask_account_card(number).replace(" ", "") ==
                expected_mask.replace(" ", ""))
    else:
        assert mask_account_card(number) == expected_mask


@pytest.mark.parametrize("date, date_tipe", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2024.03.11", "11.03.2024"),
    ("11/03/2024", "11.03.2024"),
    ("", "")
])
def test_get_date(date: str, date_tipe: str) -> None:
    assert get_date(date) == date_tipe


@pytest.mark.parametrize("state, expected", [
    ('EXECUTED', [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]),
    ('CANCELED', [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]),
    ('NON_EXISTENT', [])
])
def test_filter_by_state(banking_operations: list[dict[str, Any]], state: str, expected: list[dict[str, Any]]) -> None:
    assert filter_by_state(banking_operations, state) == expected


@pytest.mark.parametrize("state, expected", [
    ('EXECUTED', [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]),
    ('CANCELED', [
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
    ]),
    ('NON_EXISTENT', [])
])
def test_sort_by_date(date_operations_fixture, state: str, expected: list[dict[str, Any]]) -> None:
    assert sort_by_date(date_operations_fixture, state, key='desc') == expected

4. Добавлены файлы с фикстурами conftest.py и импортом необходимых словарей и функций imports.py
5. Введите данные своих транзакций для корректного отражения и анализа валюты, описания транзакции и банковской карты. Воспользуйтесь функциями filter_by_currency, transaction_descriptions, card_number_generator.

def filter_by_currency(transactions: list[dict], currency: str):
    """
    Принимает на вход список словарей, представляющих транзакции.
    Возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной.
    """
    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency:
            yield transaction

Пример использования функции:
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

>>> {
          "id": 939719570,
          "state": "EXECUTED",
          "date": "2018-06-30T02:08:58.425572",
          "operationAmount": {
              "amount": "9824.07",
              "currency": {
                  "name": "USD",
                  "code": "USD"
              }
          },
          "description": "Перевод организации",
          "from": "Счет 75106830613657916952",
          "to": "Счет 11776614605963066702"
      }


def transaction_descriptions(transactions: list[dict]):
    """
    Принимает на вход список словарей с транзакциями.
    Возвращает описание каждой операции по очереди.
    """
    for transaction in transactions:
        yield transaction['description']

Пример использования функции
descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
Входные данные:
{"description": "Перевод организации", "from": "Счет 75106830613657916952", "to": "Счет 11776614605963066702"},
{"description": "Перевод со счета на счет", "from": "Счет 19708645243227258542", "to": "Счет 75651667383060284188"},
{"description": "Перевод со счета на счет", "from": "Счет 44812258784861134719", "to": "Счет 74489636417521191160"},
{"description": "Перевод с карты на карту", "from": "Visa Classic 6831982476737658", "to": "Visa Platinum 8990922113665229"},
{"description": "Перевод организации", "from": "Visa Platinum 1246377376343588", "to": "Счет 14211924144426031657"}

>>> Перевод организации
    Перевод со счета на счет
    Перевод со счета на счет
    Перевод с карты на карту
    Перевод организации
> 

def card_number_generator(start=1, stop=9999999999999999):
    """
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX.
    """
    for num in range(start, stop + 1):
        card_number = f"{num:016}"
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_number

Пример использования функции
for card_number in card_number_generator(1, 5):
    print(card_number)

>>> 0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005

6. Проведены тесты на транзакции:

@pytest.mark.parametrize("filter_by_currency_fixture, currency, expected", [
    ([{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572",
       "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод организации", "from": "Счет 75106830613657916952",
       "to": "Счет 11776614605963066702"}], "USD",
     [{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572",
       "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод организации", "from": "Счет 75106830613657916952",
       "to": "Счет 11776614605963066702"}]),
    ([{"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878",
       "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод со счета на счет", "from": "Счет 19708645243227258542",
       "to": "Счет 75651667383060284188"}], "USD",
     [{"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878",
       "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод со счета на счет", "from": "Счет 19708645243227258542",
       "to": "Счет 75651667383060284188"}]),
    ([{"id": 873106923, "state": "EXECUTED", "date": "2019-03-23T01:09:46.296404",
       "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
       "description": "Перевод со счета на счет", "from": "Счет 44812258784861134719",
       "to": "Счет 74489636417521191160"}], "USD", []),
    ([{"id": 895315941, "state": "EXECUTED", "date": "2018-08-19T04:27:37.904916",
       "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод с карты на карту", "from": "Visa Classic 6831982476737658",
       "to": "Visa Platinum 8990922113665229"}], "USD",
     [{"id": 895315941, "state": "EXECUTED", "date": "2018-08-19T04:27:37.904916",
       "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
       "description": "Перевод с карты на карту", "from": "Visa Classic 6831982476737658",
       "to": "Visa Platinum 8990922113665229"}]),
    ([{"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689",
       "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
       "description": "Перевод организации", "from": "Visa Platinum 1246377376343588",
       "to": "Счет 14211924144426031657"}], "USD", []),
    ([], "NON_EXISTENT", [])
])
def test_filter_by_currency(filter_by_currency_fixture, currency: str, expected: list[dict[str, Any]]) -> None:
    assert list(filter_by_currency(filter_by_currency_fixture, currency)) == expected


@pytest.mark.parametrize("transactions_fixture, expected", [
    ([{"description": "Перевод организации", "from": "Счет 75106830613657916952",
       "to": "Счет 11776614605963066702"},
      {"description": "Перевод со счета на счет", "from": "Счет 19708645243227258542",
       "to": "Счет 75651667383060284188"},
      {"description": "Перевод со счета на счет", "from": "Счет 44812258784861134719",
       "to": "Счет 74489636417521191160"},
      {"description": "Перевод с карты на карту", "from": "Visa Classic 6831982476737658",
       "to": "Visa Platinum 8990922113665229"},
      {"description": "Перевод организации", "from": "Visa Platinum 1246377376343588",
       "to": "Счет 14211924144426031657"}
      ],
     ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет", "Перевод с карты на карту",
      "Перевод организации"]),
    ([], [])
])
def test_transaction_descriptions(transactions_fixture, expected: list[str]) -> None:
    assert list(transaction_descriptions(transactions_fixture)) == expected


@pytest.mark.parametrize("start, stop, expected", [
    (7000792289606361, 7000792289606361, ["7000 7922 8960 6361"]),
    (123456781234, 123456781234, ["0000 1234 5678 1234"]),
    (0, 0, ["0000 0000 0000 0000"])
])
def test_card_number_generator(start: int, stop: int, expected: list[str]) -> None:
    assert list(card_number_generator(start, stop)) == expected
