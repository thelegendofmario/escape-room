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
    backup = open('sessions_backup.txt', 'w')
    backup.write(str(sessions))
    backup.close()

def get_value(value, channelid):
    backup = open('sessions_backup.txt', 'r')
    sessions_dict = eval(backup.read())
    return sessions_dict[channelid][value]

def update_value(value,updated_value, channelid):
    backup = open('sessions_backup.txt', 'r')
    sessions = eval(backup.read())
    backup.close()
    backup = open('sessions_backup.txt', 'w')
    sessions[channelid][value] = updated_value
    backup.write(str(sessions))
    backup.close()
