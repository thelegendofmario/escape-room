def map_alpha_to_numbers(letter: str) -> int:
    '''
    maps an alphabet letter to a number starting from 1.
    '''
    letter_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}

    return letter_dict[letter]