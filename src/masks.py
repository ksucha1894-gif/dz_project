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
    # Проверяем, что номер счета достаточно длинный для маскирования
    if len(account_number) < 4:
        return "**" + account_number  # Если номер короче 4 символов, просто добавляем маску перед ним
    return f"**{account_number[-4:]}"
