import os

from typing import Dict, Any
from src.utils import load_transactions
from src.read_csv_excel import read_transaction_csv, read_transaction_excel
from src.processing import filter_by_state, sort_by_date


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    choice = input("Пользователь: ")

    # Обработка выбора источника данных
    if choice == '1':
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions(os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.json'))
    elif choice == '2':
        print("Для обработки выбран CSV-файл.")
        transactions = read_transaction_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.csv'))
    elif choice == '3':
        print("Для обработки выбран XLSX-файл.")
        transactions = read_transaction_excel(os.path.join(os.path.dirname(__file__), '..', 'data',
                                                           'transactions_excel.xlsx'))
    else:
        print("Некорректный выбор. Завершение программы.")
        return

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("Пользователь: ").strip()

        status_normalized = status_input.upper()

        if status_normalized in ['EXECUTED', 'CANCELED', 'PENDING']:
            print(f"Операции отфильтрованы по статусу \"{status_normalized}\"")
            break
        else:
            print(f"Статус операции \"{status_input}\" недоступен.")
            # повторный запрос статуса

    # Предлагаем дополнительные фильтры
    print("Отсортировать операции по дате? Да/Нет")
    sort_date_choice = input("Пользователь: ").strip().lower()
    sort_date = sort_date_choice == 'да'

    order = None
    if sort_date:
        print("Отсортировать по возрастанию или по убыванию?")
        order_input = input("Пользователь: ").strip().lower()
        if order_input == 'по возрастанию':
            order = 'asc'
        elif order_input == 'по убыванию':
            order = 'desc'

    # Фильтруем по статусу
    transactions_filtered = filter_by_state(transactions, status_normalized)

    # Сортируем по дате, если выбрано
    if order:
        transactions_sorted = sort_by_date(transactions_filtered, key=order)
    else:
        transactions_sorted = transactions_filtered

    # Фильтрация по валюте
    print("Выводить только рублёвые транзакции? Да/Нет")
    only_ruble_choice = input("Пользователь: ").strip().lower()
    only_ruble = only_ruble_choice == 'да'

    if only_ruble:
        transactions_final = [t for t in transactions_sorted if t.get('currency') == 'RUB']
    else:
        transactions_final = transactions_sorted

    # --- Добавляем фильтрацию по ключевому слову ---
    print("Введите ключевое слово для фильтрации транзакций или оставьте пустым для пропуска:")
    keyword = input("Пользователь: ").strip()

    if keyword:
        def contains_keyword(transaction: Dict[str, Any]) -> bool:
            return any(keyword.lower() in str(value).lower() for value in transaction.values())

        transactions_final = [t for t in transactions_final if contains_keyword(t)]

    # Итоговый список для отображения
    if not transactions_final:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print("\nРаспечатываю итоговый список транзакций...\n")
        print(f"Всего банковских операций в выборке: {len(transactions_final)}")
        for t in transactions_final:
            print(t)
