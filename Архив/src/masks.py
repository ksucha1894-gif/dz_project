def get_mask_card_number(number: str) -> str:
    """
    Функция принимает число - номер карты
    Маска
    преобразует число в формат XXXX XX** **** XXXX
    """
    masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает номер карты
    Маска преобразует номер карты в формат **XXXX
    """
    return f"**{account_number[-4:]}"
