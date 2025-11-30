import unittest
from unittest.mock import Mock, patch

import requests

from src.external_api import convert_to_rubles


class TestConvertToRubles(unittest.TestCase):

    @patch('requests.get')
    @patch('os.getenv')
    def test_convert_rub(self, mock_getenv: Mock, mock_requests_get: Mock) -> None:
        # Валюта RUB, деньги остаются теми же
        transaction = {'amount': '100', 'currency': 'RUB'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        self.assertEqual(result, 100)

    @patch('requests.get')
    @patch('os.getenv')
    def test_convert_usd_success(self, mock_getenv: Mock, mock_requests_get: Mock) -> None:
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
    def test_convert_eur_success(self, mock_getenv: Mock, mock_requests_get: Mock) -> None:
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
    def test_api_request_exception(self, mock_getenv: Mock, mock_requests_get: Mock) -> None:
        mock_getenv.return_value = 'fake_api_key'
        # Имитируем RequestException
        mock_requests_get.side_effect = requests.exceptions.RequestException("API error")

        transaction = {'amount': '10', 'currency': 'USD'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        # В случае ошибки возвращается исходная сумма
        self.assertEqual(result, 10)

    @patch('requests.get')
    @patch('os.getenv')
    def test_missing_currency_key(self, mock_getenv: Mock, mock_requests_get: Mock) -> None:
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
    def test_unknown_currency(self, mock_getenv: Mock, mock_requests_get: Mock) -> None:
        # Валюта не из списка
        transaction = {'amount': '7', 'currency': 'GBP'}
        result = convert_to_rubles(transaction, 'http://fakeapi.com/rates')
        # В случае неизвестной валюты возвращается исходная сумма
        self.assertEqual(result, 7)


if __name__ == '__main__':
    unittest.main()
