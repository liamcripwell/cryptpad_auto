import re
import json
import string
import random

import pandas as pd


def rand_uid(blacklist=[]):
    while True:
        uid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=11))
        if uid not in blacklist:
            break
    return uid

def is_uid(xs):
    uid_pat = r"[a-z0-9]{11}$"
    return bool(re.match(uid_pat, xs))

def needs_uid(obj):
    if any([k in obj.keys() for k in ["type"]]):
        return False
    elif any([k in obj.keys() for k in ["v"]]):
        return True
    return False

def strip_key_r(obj, key):
    """Recursively strip a key from a dict-like object."""
    if isinstance(obj, dict):
        if key in obj:
            del obj[key]
        for k, v in obj.items():
            obj[k] = strip_key_r(v, key)
    elif isinstance(obj, list):
        obj = [strip_key_r(v, key) for v in obj]
    return obj

def get_data_iterator(data):
    if isinstance(data, list):
        data_iter = enumerate(data)
    elif isinstance(data, pd.DataFrame):
        data_iter = data.iterrows()

    return data_iter

def read_data_file(data):
    if isinstance(data, str):
        if data.endswith(".json"):
            data = json.load(open(data, "r"))
        elif data.endswith(".csv"):
            data = pd.read_csv(data)
    return data