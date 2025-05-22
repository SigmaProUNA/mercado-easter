"""
Esse arquivo é para calculos de matemática financeiras. 
"""



# Padoes da industria financeira
class Standards:
    INTERNATIONAL_SEP = "."
    BR_SEP = ","


# Converte centavos para dinheiro humano e retorna como float
def cents_to_money(cents: int | str, money_unit: str = "R$", decimal_place: int = 2, separator_standard: str = Standards.BR_SEP) -> str:
    cents = str(cents)[::-1] # Inverter a string
    cents = cents[decimal_place:][::-1].zfill(1)  + separator_standard + cents[0:decimal_place][::-1].zfill(2) # Separar os centavos 
    
    return money_unit + " " + cents


# Consegue o valor de lucro
def get_profit(profit_rate: float, base_price: float) -> float:
    return base_price * profit_rate


# Adiciona o lucro ao preco base
def add_profit(profit_rate: float, base_price: float) -> float:
    return base_price + get_profit(profit_rate, base_price)


if __name__ == "__main__":
    print(cents_to_money(1000))
    