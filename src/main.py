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
        # Вызов функции загрузки из JSON
        transactions = load_transactions()
    elif choice == '2':
        print("Для обработки выбран CSV-файл.")
        # Вызов функции загрузки из CSV
        transactions = read_transaction_csv()
    elif choice == '3':
        print("Для обработки выбран XLSX-файл.")
        # Вызов функции загрузки из XLSX
        transactions = read_transaction_excel()
    else:
        print("Некорректный выбор. Завершение программы.")
        return

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("Пользователь: ").strip()

        # Нормализация статуса
        status_normalized = status_input.upper()

        if status_normalized in ['EXECUTED', 'CANCELED', 'PENDING']:
            print(f"Операции отфильтрованы по статусу \"{status_normalized}\"")
            break
        else:
            print(f"Статус операции \"{status_input}\" недоступен.")
            # Повторный запрос статуса

    # Предлагаем дополнительные фильтры
    # Отсортировать по дате?
    print("Отсортировать операции по дате? Да/Нет")
    sort_date_choice = input("Пользователь: ").strip().lower()
    sort_date = sort_date_choice == 'да'

    # По возрастанию или убыванию
    order = None
    if sort_date:
        print("Отсортировать по возрастанию или по убыванию?")
        order_input = input("Пользователь: ").strip().lower()
        if order_input.lower() == 'по возрастанию':
            order = 'asc'
        elif order_input.lower() == 'по убыванию':
            order = 'desc'

    # Предварительно фильтруем по статусу, использую функцию filter_by_state
    transactions_filtered = filter_by_state(transactions, status_normalized)

    # Далее сортируем по дате, если выбран сортировка
    if order:
        transactions_sorted = sort_by_date(transactions_filtered, key=order)
    else:
        transactions_sorted = transactions_filtered

    # Предлагаем фильтрацию по валюте
    print("Выводить только рублёвые транзакции? Да/Нет")
    only_ruble_choice = input("Пользователь: ").strip().lower()
    only_ruble = only_ruble_choice == 'да'

    # Фильтрация по валюте (только рубли)
    if only_ruble:
        transactions_final = [t for t in transactions_sorted if t.get('currency') == 'RUB']
    else:
        transactions_final = transactions_sorted

    # Возвращаем итоговый список для отображения
    filtered_transactions = transactions_final

    # Далее вывод:
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print("\nРаспечатываю итоговый список транзакций...\n")
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for t in filtered_transactions:
            print(t)
