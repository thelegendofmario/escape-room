sessions = {}

def map_alpha_to_numbers(letter: str) -> int:
    '''
    maps an alphabet letter to a number starting from 1.
    '''
    letter_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}

    return letter_dict[letter]

# first_answer_encoded = ''
# first_answer = ''
# first_puzzle_complete = False
# has_key = False

# second_puzzle_finished = False

def initialize_new_session(channelid):
    sessions.update({f'{channelid}': {'first_answer_encoded': '', 'first_answer': '', 'first_puzzle_complete': False, 'has_key': False, 'second_puzzle_finished': False}})

def get_value(value, channelid):
    return sessions[channelid][value]

def update_value(value,updated_value, channelid):
    sessions[channelid][value] = updated_value