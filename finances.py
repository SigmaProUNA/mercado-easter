# Padoes da industria financeira
class Standards:
    INTERNATIONAL_SEP = "."
    BR_SEP = ","


# Converte centavos para dinheiro humano e retorna como float
def cents_to_money(cents: int, money_unit: str = "R$", decimal_place: int = 2, separator_standard: str = Standards.BR_SEP) -> str:
    cents = str(cents)[::-1] # Inverter a string
    cents = cents[0:decimal_place] + separator_standard + cents[decimal_place:]# Separar os centavos 
    
    return money_unit + " " + cents[::-1]


# Consegue o valor de lucro
def get_profit(profit_rate: float, base_price: float) -> float:
    return base_price * profit_rate


# Adiciona o lucro ao preco base
def add_profit(profit_rate: float, base_price: float) -> float:
    return base_price + get_profit(profit_rate, base_price)


if __name__ == "__main__":
    print(cents_to_money(1000))
    