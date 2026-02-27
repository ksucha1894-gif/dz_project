import unittest
import random

from src.operations_re import process_bank_search, process_bank_operations


class TestProcessBankOperations(unittest.TestCase):

    def setUp(self):
        self.categories = ['utilities', 'salary', 'transfer', 'grocery']
        self.data = [
            {'description': 'Payment to utilities'},  # utilities
            {'description': 'Salary from employer'},  # salary
            {'description': 'Transfer to savings account'},  # transfer
            {'description': 'Grocery shopping at supermarket'},  # grocery
            {'description': 'Random payment'}  # не совпадает, random category
        ]

    def test_counts_with_exact_and_random(self):
        random.seed(42)  # фиксация seed для воспроизводимости
        result = process_bank_operations(self.data, self.categories)

        # Сумма счетчиков должна равняться числу операций (строк в data)
        self.assertEqual(sum(result.values()), len(self.data))

        # Должны быть все категории (поскольку последняя запись распределена рандомно)
        for cat in self.categories:
            self.assertIn(cat, result)

        # Проверяем конкретный ожидаемый результат с seed=42
        expected = {
            'utilities': 1,
            'salary': 1,
            'transfer': 1,
            'grocery': 2  # последняя "Random payment" с этим сидом попала в grocery
        }
        self.assertEqual(result, expected)

    def test_no_matches_all_random(self):
        random.seed(1)
        data = [
            {'description': 'Unknown operation 1'},
            {'description': 'Something else'},
        ]
        result = process_bank_operations(data, self.categories)
        # В этом случае обе операции отнесены рандомно
        self.assertEqual(sum(result.values()), len(data))

    def test_empty_data(self):
        result = process_bank_operations([], self.categories)
        self.assertEqual(result, {})  # Пустой словарь, т.к. не было операций

    def test_empty_categories_raises(self):
        with self.assertRaises(IndexError):
            # random.choice(categories) вызовет ошибку, если categories пуст
            process_bank_operations(self.data, [])


if __name__ == '__main__':
    unittest.main()