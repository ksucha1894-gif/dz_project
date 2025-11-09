from imports import (Any, filter_by_state, get_date, get_mask_account, get_mask_card_number, mask_account_card, pytest,
                     sort_by_date)


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
def test_sort_by_date(date_operations: list[dict[str, Any]], state: str, expected: list[dict[str, Any]]) -> None:
    assert sort_by_date(date_operations, state, key='desc') == expected
