import logging
import re

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