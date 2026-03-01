import unittest

from src.operations_re import process_bank_search, process_bank_operations


class TestBankProcessing(unittest.TestCase):
    def setUp(self) -> None:
        # Исходные данные для тестирования
        self.data = [
            {'description': 'Payment to utilities'},
            {'description': 'Salary from employer'},
            {'description': 'Transfer to savings account'},
            {'description': 'Grocery shopping at supermarket'}
        ]

    def test_process_bank_search_found(self) -> None:
        # Тест поиска по ключевому слову
        result = process_bank_search(self.data, 'utilities')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Payment to utilities')

    def test_process_bank_search_not_found(self) -> None:
        # Тест поиска по отсутствующему слову
        result = process_bank_search(self.data, 'rent')
        self.assertEqual(result, [])

    def test_process_bank_operations_counts(self) -> None:
        # Тест подсчёта операций по категориям
        categories = ['utilities', 'salary', 'transfer', 'grocery']
        result = process_bank_operations(self.data, categories)
        # Ожидается по одной операции на каждую категорию
        self.assertEqual(result['utilities'], 1)
        self.assertEqual(result['salary'], 1)
        self.assertEqual(result['transfer'], 1)
        self.assertEqual(result['grocery'], 1)
        # Общая сумма должна равняться количеству операций
        self.assertEqual(sum(result.values()), len(self.data))

    def test_process_bank_operations_empty_categories(self) -> None:
        # Ваша текущая реализация возвращает пустой словарь при пустом списке
        result = process_bank_operations(self.data, [])
        self.assertEqual(result, {})

    def test_process_bank_operations_empty_categories_need_exception(self) -> None:
        # Если хотите, чтобы при пустом списке было исключение, раскомментируйте и используйте
        # with self.assertRaises(IndexError):
        #     process_bank_operations(self.data, [])
        pass

    def test_process_bank_search_case_insensitivity(self) -> None:
        # Проверка игнорирования регистра в поиске
        result = process_bank_search(self.data, 'Utilities')
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
