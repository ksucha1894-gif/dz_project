from src.masks import get_mask_card_number, get_mask_account


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


def get_date(date_tipe: str) -> str:
    """
       Функция принимает строку с датой в формате "2024-03-11T02:26:18.67140
       Функция возвращает строку с датой в формате "ДД.ММ.ГГГГ"
    """
    return f'{date_tipe[8:10]}.{date_tipe[5:7]}.{date_tipe[:4]}'
