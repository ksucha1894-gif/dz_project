import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.read_csv_excel import read_transaction_csv, read_transaction_excel


class TestReadTransactionCsv(unittest.TestCase):

    @patch("csv.DictReader")
    @patch("builtins.open", new_callable=mock_open, read_data="date;amount\n2021-01-01;100\n2021-01-02;200")
    def test_read_csv_success(
            self,
            mock_open_obj: MagicMock,
            mock_csv_reader: MagicMock
    ) -> None:
        # Настраиваем возврат словарей при чтении csv
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

        # Проверка, что open вызван с правильным путём и кодировкой
        mock_open_obj.assert_called_once_with("dummy_path.csv", encoding='utf-8')
        # Проверка, что csv.DictReader вызван
        mock_csv_reader.assert_called()

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
