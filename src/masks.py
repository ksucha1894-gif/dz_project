import logging
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))  # Определяем путь в корневую папку проекта

rel_file_path = os.path.join(current_dir, "../logs/masks.log")  # Определяем относительный путь к файлу
abs_file_path = os.path.abspath(rel_file_path)  # Определяем абсолютный путь в файлу

logger = logging.getLogger('masks')
# Автоматически вставляем абсолютный путь к файлу для корректной работы
file_handler = logging.FileHandler(abs_file_path)
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
    if not number:
        return ' ** **** '
    else:
        logger.error('Введены недопустимые символы в номере карты')
        return ""


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает номер счета.
    Маска преобразует номер счета в формат **XXXX.
    Если в номере есть нецифровые символы, логирует ошибку.
    """
    if account_number == '':
        return '**'
    # Поиск последних четырех цифр
    last_four_digits = re.search(r'(\d{0,4})$', account_number)
    if last_four_digits and last_four_digits.group():
        logger.info(f"Маскировка номера счета: последние 4 символа '{last_four_digits.group()}'")
        return f"**{last_four_digits.group()}"
    else:
        logger.error(f"В номере счета обнаружены недопустимые символы: '{account_number}'")
        return "Ошибка: номер счета содержит недопустимые символы."


if __name__ != "__main__":
    print(get_mask_card_number("1234567812345678"))
    print(get_mask_account("12345678"))
