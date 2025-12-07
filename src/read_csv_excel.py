import csv
from typing import Dict, List

import pandas as pd


def read_transaction_csv(file_path: str) -> List[Dict[str, str]]:
    """Читает CSV-файл с транзакциями и возвращает список словарей."""
    try:
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            return [row for row in reader]
    except FileNotFoundError:
        return []


# Вызов функции с нужным путем к файлу
transactions_list = read_transaction_csv('/Users/ksenia/Desktop/PYTHON/transactions.csv')
print(transactions_list)


def read_transaction_excel(excel_path: str) -> List[Dict]:
    """Функция принимает путь к файлу формата excel и возвращает список словарей."""
    try:
        excel_data = pd.read_excel(excel_path)
        return excel_data.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл не найден: {excel_path}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []


# Вызов функции с нужным путем к файлу
excel_path = '/Users/ksenia/Desktop/PYTHON/transactions_excel.xlsx'
transactions_excel = read_transaction_excel(excel_path)
print(transactions_excel)
