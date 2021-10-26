import re
import json
from copy import deepcopy

from cryptpad_generation.utils import rand_uid, needs_uid


def sub_values(obj, data):
    flag_pat = r'\$([a-zA-z0-9]+)\$'
    
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = sub_values(obj[i], data)
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = sub_values(value, data)
        # TODO: need to keep log of used uids
        if needs_uid(obj):
            obj["uid"] = rand_uid()
    elif isinstance(obj, str):
        obj = re.sub(flag_pat,
                lambda m: str(data.get(m.group(1), m.group(0))), obj)

    return obj

def generate_form(data, template):
    # load template from file
    if isinstance(template, str):
        template = json.load(open(template, "r"))

    doc = {
        "form": {},
        "order": [],
        "version": 1
    }

    results = []
    for component in template:
        if component["type"] == "from_data":
            for row in data:
                for sub_component in component["body"]:
                    results.append(sub_values(deepcopy(sub_component), row))
        else:
            results.append(component)
        
    for component in results:
        uid = rand_uid()
        doc["form"][uid] = component
        doc["order"].append(uid)

    return doc

