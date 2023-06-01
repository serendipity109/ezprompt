import random
import string


def generate_random_id(n=10):
    letters_and_digits = string.digits
    random_id = "".join(random.choice(letters_and_digits) for _ in range(n))
    return random_id
