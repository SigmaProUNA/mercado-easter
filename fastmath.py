"""
Biblioteca para funções matemáticas rápidas
"""

separators = [",", ".", "/"]

# Verifica se o número é um inteiro (sem sinal)
def is_integer(s: str) -> bool:
    return s.isdigit() if s else False

# Verifica se o número é um float com vírgula ou uma fração com barra
def is_number(s: str) -> bool:
    if not s:
        return False

    # Verifica se é um inteiro
    if s.isdigit():
        return True

    # Verifica se é um float com vírgula ou ponto (ex: "3,14") 
    for sep in separators:
        if sep in s:
            parts = s.split(sep)
            return len(parts) == 2 and all(p.isdigit() for p in parts)
    
    #if "," in s:
    #    partes = s.split(",")
    #    return len(partes) == 2 and all(p.isdigit() for p in partes)

    # Verifica se é uma fração com barra (ex: "3/4")
    #if "/" in s:
    #    partes = s.split("/")
    #    return len(partes) == 2 and all(p.isdigit() for p in partes)

    return False


# Verificar se é um padrão numerico
def is_money(s: str) -> bool:
    if not is_number(s):
        return False
    else:
        for sep in separators:
            parts = s.split(sep)
            if len(parts) == 2:
                if len(parts[1]) >= 2:
                    return True
                else:
                    return False
