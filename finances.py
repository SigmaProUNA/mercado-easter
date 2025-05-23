"""
Esse arquivo é para calculos de matemática financeiras. 
"""



# Padoes da industria financeira
class Standards:
    INTERNATIONAL_SEP = "."
    BR_SEP = ","


# Converte centavos para dinheiro humano e retorna como float
def cents_to_money(cents: int | str, money_unit: str = "R$", decimal_place: int = 2, separator_standard: str = Standards.BR_SEP) -> str:
    cents = str(cents)
    
    money = ""
    
    # Inserir o separador
    money = [c for c in cents]
    separator_index = (len(cents)-decimal_place)
    money.insert(separator_index, separator_standard)
    money = "".join(money)
    
    # Adicionar zeros 
    integer_part, cent_part = money.split(separator_standard)
    money = integer_part.zfill(1) + separator_standard 
    
    if len(cents) == 1:
        cent_part = "0" + cent_part
    elif len(cents) == 0:
        cent_part = "00"
        
    if len(cent_part) < decimal_place:
        cent_part += "0" * (decimal_place - len(cent_part))
    
    money += cent_part
    
    return money_unit + " " + money


# Converte o valor em unidades humanas para números amigaveis para computadores
def money_to_cents(money: str, separator_standard: str = Standards.BR_SEP) -> int:
    conv_money = ""
    for char in money:
        if char in "0123456789":
            conv_money += char

    if conv_money == "":
        conv_money = "0"

    return int(conv_money)


# Consegue o valor de lucro
def get_profit(profit_rate: float, base_price: int) -> int:
    return round(base_price * profit_rate)


# Adiciona o lucro ao preco base
def add_profit(profit_rate: float, base_price: int) -> int:
    return round(base_price + get_profit(profit_rate, base_price))


if __name__ == "__main__":
    pass
    