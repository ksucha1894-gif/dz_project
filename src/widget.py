def mask_account_card(card_tipe_number: str) -> str:
    """
       Функция, которая принимает тип и число - тип и номер карты, тип и номер расчетного счета
       Маска, которая преобразует тип и число в формат тип XXXX XX** **** XXXX или в **XXXX
       """
    card_info = card_tipe_number.split(' ', 1)
    if 'счет' in card_info[0].lower():
        masked_account = f"{card_info[0]} **{card_info[1][-4:]}"
        return masked_account
    else:
        masked_number = f"{card_info[0]} {card_info[1][:4]} {card_info[1][4:6]}** **** {card_info[1][-4:]}"
        return masked_number


card_tipe_number = "Visa Platinum 7000792289606361"
print(mask_account_card(card_tipe_number))
