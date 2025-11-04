from src.masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(number: str) -> str:
    """
       Функция принимает строку с типом и номером: "Карта <номер>" или "Счет <номер>"
       Маска преобразует номер в формат "тип XXXX XX** **** XXXX" или "тип **XXXX"
       """
    # Проверка на пустую строку или строку, содержащую только пробелы
    if not number.strip():
        return ""

    card_info, number = number.rsplit(' ', maxsplit=1)
    if 'счет' in card_info.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f'{card_info} {masked_number}'


def get_date(date_tipe: str) -> str:
    """
       Функция принимает строку с датой и возвращает строку с датой в формате "ДД.ММ.ГГГГ".
    """
    # Попробуем определить формат даты по длине строки или по наличию символов
    if "-" in date_tipe and "T" in date_tipe:
        # Если формат "2024-03-11T02:26:18.671407"
        return f'{date_tipe[8:10]}.{date_tipe[5:7]}.{date_tipe[:4]}'
    else:
        # Иначе используем datetime для других форматов
        for fmt in ("%d.%m.%Y", "%Y.%m.%d", "%d/%m/%Y"):
            try:
                date_obj = datetime.strptime(date_tipe, fmt)
                return date_obj.strftime("%d.%m.%Y")
            except ValueError:
                continue
    # Если формат не подошел, возвращаем пустую строку или поднимаем ошибку
    return ""
