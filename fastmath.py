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


def is_number(x: str) -> bool:
    valid_separators = [44, 47]

    for char in x:
        char_num = ord(char)

        if is_integer(char) or char_num in valid_separators:
            continue
        else:
            return False
        
    return True
    