import json
import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions


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
