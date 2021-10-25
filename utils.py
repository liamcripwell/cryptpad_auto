import string
import random


def rand_uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=11))