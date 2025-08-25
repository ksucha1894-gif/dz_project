def get_mask_card_number(card_number: str) -> str:
    """
    Функция, которая принимает число - номер карты
    Маска, которая преобразует число в формат XXXX XX** **** XXXX
    """
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked_number


card_number: str = "7000792289606361"
print(get_mask_card_number(card_number))
