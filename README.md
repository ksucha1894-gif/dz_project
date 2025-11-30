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

7. Добавлен декоратор и проведена проверка его работы тестами

def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функции.
    Если задан `filename`, лог записывается в файл, иначе выводится в консоль.
    """
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            """Логирование начала и конца выполнения функции, а также ее результаты или возникшие ошибки"""
            try:
                start_time = time()
                result = func(*args, **kwargs)
                end_time = time()
                log_message = (f"Функция: {func.__name__}\n Время начала выполнения функции: {start_time}\n "
                               f"Время окончания выполнения функции: {end_time}\n Результат: {result}\n")
                if filename:
                    with open(filename, "a") as log_file:
                        log_file.write(log_message)
                else:
                    print(log_message)
                return result

            except Exception as e:
                error_message = f'{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}'
                if filename:
                    with open(filename, "a") as log_file:
                        log_file.write(error_message)
                else:
                    print(error_message)
                raise

        return inner

    return wrapper

@log(None)
def add(x: int, y: int) -> int:
    return x + y


def test_add_log_output(capsys: pytest.CaptureFixture[str]) -> None:
    add(1, 2)
    captured = capsys.readouterr()
    assert "Функция: add" in captured.out
    assert "Результат: 3" in captured.out


def test_add_log_to_file(tmp_path: Any) -> None:
    log_file = tmp_path / "mylog.txt"

    @log(log_file)
    def add_func(x: int, y: int) -> int:
        return x + y

    add_func(1, 2)

    with open(log_file, "r") as f:
        content = f.read()
        assert "Функция: add_func" in content
        assert "Результат: 3" in content


@log(None)
def error_func(x: int, y: int) -> float:
    return x / y


def test_error_logging(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ZeroDivisionError):
        error_func(1, 0)
    captured = capsys.readouterr()
    assert "error_func" in captured.out
    assert "division by zero" in captured.out

8. Добавлена функция, которая загружает данные о финансовых транзакциях из JSON-файла, и проведены тесты:
def load_transactions(filepath: str) -> List[Dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл по пути '{filepath}' не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Файл '{filepath}' содержит некорректный JSON.")
        return []
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return []

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data
    else:
        print(f"Ошибка: Данные в файле '{filepath}' не являются списком словарей.")
        return []

Тесты:
class TestLoadTransactions(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_load_correct_data(self, mock_file):
        # Мокаем корректные данные (список словарей)
        mock_data = [
            {"date": "2023-10-01", "amount": 100, "description": "Test"}
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_data)

        result = load_transactions('data/operations.json')
        self.assertEqual(result, mock_data)
        mock_file.assert_called_with('data/operations.json', 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_file):
        # Вызовем исключение, чтобы эмулировать отсутствие файла
        mock_file.side_effect = FileNotFoundError
        result = load_transactions('data/operations.json')
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_invalid_json(self, mock_file):
        # Устанавливаем некорректный JSON
        mock_file.return_value.read.return_value = "{invalid_json:}"

        result = load_transactions('data/operations.json')
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_data_is_not_list(self, mock_file):
        # JSON-данные — не список
        mock_file.return_value.read.return_value = json.dumps({"key": "value"})
        result = load_transactions('data/operations.json')
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_list_contains_non_dicts(self, mock_file):
        # список, содержащий не словари
        mock_file.return_value.read.return_value = json.dumps([1, 2, 3])
        result = load_transactions('data/operations.json')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()

9. Добавлена функция, которая конвертирует сумму транзакции в рубли, используя курсы валют из внешнего API, и проведено ее тестирование:
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

Тесты:
class TestConvertToRubles(unittest.TestCase):

    @patch('requests.get')
    @patch('os.getenv')
    def test_convert_rub(self, mock_getenv, mock_requests_get):
        # Валюта RUB, деньги остаются теми же
        transaction = {'amount': '100', 'currency': 'RUB'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        self.assertEqual(result, 100)

    @patch('requests.get')
    @patch('os.getenv')
    def test_convert_usd_success(self, mock_getenv, mock_requests_get):
        # Замокаем переменную окружения API_KEY
        mock_getenv.return_value = 'fake_api_key'
        # Мокаем успешный ответ API с курсом USD
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {'USD': 75.0}
        mock_requests_get.return_value = mock_response

        transaction = {'amount': '2', 'currency': 'USD'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        self.assertAlmostEqual(result, 2 * 75.0)

    @patch('requests.get')
    @patch('os.getenv')
    def test_convert_eur_success(self, mock_getenv, mock_requests_get):
        # Замокаем переменную окружения API_KEY
        mock_getenv.return_value = 'fake_api_key'
        # Мокаем успешный ответ API с курсом EUR
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {'EUR': 90.0}
        mock_requests_get.return_value = mock_response

        transaction = {'amount': '3', 'currency': 'EUR'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        self.assertAlmostEqual(result, 3 * 90.0)

    @patch('requests.get')
    @patch('os.getenv')
    def test_api_request_exception(self, mock_getenv, mock_requests_get):
        mock_getenv.return_value = 'fake_api_key'
        # Имитируем RequestException
        mock_requests_get.side_effect = requests.exceptions.RequestException("API error")

        transaction = {'amount': '10', 'currency': 'USD'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        # В случае ошибки возвращается исходная сумма
        self.assertEqual(result, 10)

    @patch('requests.get')
    @patch('os.getenv')
    def test_missing_currency_key(self, mock_getenv, mock_requests_get):
        mock_getenv.return_value = 'fake_api_key'
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        # Отсутствует ключ 'EUR' в ответе
        mock_response.json.return_value = {}
        mock_requests_get.return_value = mock_response

        transaction = {'amount': '5', 'currency': 'EUR'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        # При KeyError возвращается исходная сумма
        self.assertEqual(result, 5)

    @patch('requests.get')
    @patch('os.getenv')
    def test_unknown_currency(self, mock_getenv, mock_requests_get):
        # Валюта не из списка
        transaction = {'amount': '7', 'currency': 'GBP'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        # В случае неизвестной валюты возвращается исходная сумма
        self.assertEqual(result, 7)


if __name__ == '__main__':
    unittest.main()

10. Добавлены логеры в файлы masks и utils:
logger = logging.getLogger('masks')
file_handler = logging.FileHandler('../logs/masks.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(number: str) -> str:
    """
    Функция принимает число - номер карты.
    Маска преобразует число в формат XXXX XX** **** XXXX.
    Если в номере есть недопустимые символы, логирует ошибку.
    """
    if re.fullmatch(r"\d+", number):  # Проверяем, что введены только цифры
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        print("Логирование начинается")
        logger.info('Маскировка номера банковской карты')
        return masked_number
    else:
        logger.error('Введены недопустимые символы в номере карты')
        return ""


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает номер счета.
    Маска преобразует номер счета в формат **XXXX.
    Если в номере есть нецифровые символы, логирует ошибку.
    """
    if not account_number.isdigit():
        logger.error(f"В номере счета обнаружены недопустимые символы: '{account_number}'")
        return "Ошибка: номер счета содержит недопустимые символы."

    if len(account_number) < 4:
        logger.info(f"Номер счета слишком короткий для маскировки: '{account_number}'. Возвращается маска.")
        return "**" + account_number
    else:
        logger.info(f"Маскировка номера счета: последние 4 символа '{account_number[-4:]}'")
        return f"**{account_number[-4:]}"


if __name__ != "__main__":
print(get_mask_card_number("1234567812345678"))
print(get_mask_account("12345678"))

logger = logging.getLogger('utils')
file_handler = logging.FileHandler('../logs/utils.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_transactions(filepath: str) -> List[Dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            logger.info(f"Попытка открытия файла: '{filepath}'.")
            data = json.load(f)
            logger.info(f"Успешно загружены данные из файла: '{filepath}'.")
    except FileNotFoundError:
        logger.error(f"Файл по пути '{filepath}' не найден.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Файл '{filepath}' содержит некорректный JSON.")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при загрузке файла '{filepath}': {e}")
        return []

    # Проверка структуры данных
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        logger.info(f"Данные в файле '{filepath}' успешно проверены и имеют правильную структуру.")
        return data
    else:
        logger.error(f"Данные в файле '{filepath}' не являются списком словарей.")
        return []

11. Созданы функции чтения о финансовых операций из CSV- и XLSX-файлов:

def read_transaction_csv(file_path: str) -> List[Dict[str, str]]:
    """Читает CSV-файл с транзакциями и возвращает список словарей."""
    try:
        with open(file_path) as file:
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

12. Созданы тесты для проверки функций чтения о финансовых операций из CSV- и XLSX-файлов:

class TestReadTransactionCsv(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="date;amount\n2021-01-01;100\n2021-01-02;200")
    @patch("csv.DictReader")
    def test_read_csv_success(self, mock_csv_reader: unittest.mock.Mock, mock_open: unittest.mock.Mock) -> None:
        # Настраиваем возврат словарей
        mock_csv_instance = MagicMock()
        mock_csv_instance.__iter__.return_value = iter([
            {'date': '2021-01-01', 'amount': '100'},
            {'date': '2021-01-02', 'amount': '200'}
        ])
        mock_csv_reader.return_value = mock_csv_instance

        result = read_transaction_csv("dummy_path.csv")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['date'], '2021-01-01')
        self.assertEqual(result[1]['amount'], '200')

        mock_open.assert_called_once_with("dummy_path.csv")
        mock_csv_reader.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_csv_file_not_found(self, mock_open: unittest.mock.Mock) -> None:
        result = read_transaction_csv("nonexistent.csv")
        self.assertEqual(result, [])


class TestReadTransactionExcel(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_read_excel_success(self, mock_read_excel: unittest.mock.Mock) -> None:
        # Создаём фейковый DataFrame и его возвращение
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {'date': '2021-01-01', 'amount': 100},
            {'date': '2021-01-02', 'amount': 200}
        ]
        mock_read_excel.return_value = mock_df

        result = read_transaction_excel("dummy_excel.xlsx")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['date'], '2021-01-01')

        mock_read_excel.assert_called_once_with("dummy_excel.xlsx")
        mock_df.to_dict.assert_called_once_with(orient="records")

    @patch("pandas.read_excel", side_effect=FileNotFoundError)
    def test_read_excel_file_not_found(self, mock_read_excel: unittest.mock.Mock) -> None:
        result = read_transaction_excel("not_exist.xlsx")
        self.assertEqual(result, [])

    @patch("pandas.read_excel", side_effect=Exception("Other error"))
    def test_read_excel_other_exception(self, mock_read_excel: unittest.mock.Mock) -> None:
        result = read_transaction_excel("error.xlsx")
        self.assertEqual(result, [])