'''
Biblioteca para funções matemáticas rápidas
'''

# Verifica se o numbero é inteiro
def is_integer(x: str) -> bool:
    valid_chars_range = [48, 57]
    
    
    for char in x:
        if ord(char) < valid_chars_range[0] or ord(char) > valid_chars_range[1]:
            return False
    return True
