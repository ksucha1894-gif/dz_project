from typing import Any

import pytest

from src.generators import filter_by_currency
from src.masks import get_mask_account, get_mask_card_number
from src.processing import sort_by_date
from src.widget import get_date, mask_account_card


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
def test_filter_by_currency(filter_by_currency_fixture: list[dict[str, Any]], currency: str,
                            expected: list[dict[str, Any]]) -> None:
    assert list(filter_by_currency(filter_by_currency_fixture, currency)) == expected


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
def test_sort_by_date(date_operations_fixture: list[dict[str, Any]], state: str,
                      expected: list[dict[str, Any]]) -> None:
    assert sort_by_date(date_operations_fixture, state, key='desc') == expected
