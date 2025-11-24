import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def convert_to_rubles(transaction: Dict[str, str], api_url: str) -> float:
    """Конвертирует сумму транзакции в рубли, используя курсы валют из внешнего API."""
    amount = float(transaction['amount'])
    currency = transaction['currency'].upper()

    if currency == 'RUB':
        return amount
    elif currency in ('USD', 'EUR'):
        try:
            response = requests.get(api_url, headers={'apikey': API_KEY})
            response.raise_for_status()
            rates = response.json()

            # Проверяем наличие ключа перед использованием
            if currency in rates:
                rate = rates[currency]
                if rate is not None:
                    return float(amount * rate)
                else:
                    # Если ключ есть, но значение None — возвращаем исходную сумму
                    print(f"Ключ {currency} есть, но значение равно None.")
                    return amount
            else:
                # Ключа нет в ответе
                print(f"Ключ {currency} отсутствует в ответе API.")
                return amount

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении курса валют: {e}")
            return amount
        except ValueError as e:
            print(f"Некорректное значение курса: {e}")
            return amount
    else:
        print(f"Неизвестная валюта: {currency}")
        return amount
