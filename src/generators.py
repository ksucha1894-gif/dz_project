from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    Принимает на вход список словарей, представляющих транзакции.
    Возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной.
    """
    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    Принимает на вход список словарей с транзакциями.
    Возвращает описание каждой операции по очереди.
    """
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(start: int = 1, stop: int = 9999999999999999) -> Iterator[str]:
    """
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX.
    """
    for num in range(start, stop + 1):
        card_number = f"{num:016}"
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_number
