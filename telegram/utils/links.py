import string


def is_correct(answer):
    for char in answer:
        if char not in string.ascii_uppercase + string.ascii_lowercase + '1234567890':
            return False
    return True
