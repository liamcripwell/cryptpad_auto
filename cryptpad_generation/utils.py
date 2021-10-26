import re
import string
import random


def rand_uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=11))

def is_uid(xs):
    uid_pat = r"[a-z0-9]{11}$"
    return bool(re.match(uid_pat, xs))


def needs_uid(obj):
    if any([k in obj.keys() for k in ["type"]]):
        return False
    elif any([k in obj.keys() for k in ["v"]]):
        return True
    return False
