from imports import Any, card_number_generator, filter_by_currency, pytest, transaction_descriptions


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
