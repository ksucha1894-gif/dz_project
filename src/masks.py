def get_mask_card_number(number: str) -> str:
    """
    Функция принимает число - номер карты
    Маска
    преобразует число в формат XXXX XX** **** XXXX
    """
    masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    return masked_number


card_number: str = "7000792289606361"
print(get_mask_card_number(card_number))


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает номер карты
    Маска преобразует номер карты в формат **XXXX
    """
    return f"**{account_number[-4:]}"


card_tipe_number = "73654108430135874305"
print(get_mask_account(card_tipe_number))
