import re
import json
from copy import deepcopy
from typing import Any, Dict

from cryptpad_generation.utils import rand_uid, needs_uid


class FormBuilder():

    FLAG = r'\$([a-zA-z0-9]+)\$'

    def __init__(self, template) -> Any:
        if isinstance(template, str):
            template = json.load(open(template, "r"))
        self.template = template
        self.reset()

    def reset(self) -> Any:
        self.doc = {
            "form": {},
            "order": [],
            "version": 1
        }

    def sub_values(self, obj, data) -> Any:
        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = self.sub_values(obj[i], data)
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self.sub_values(value, data)
            # TODO: need to keep log of used uids
            if needs_uid(obj):
                obj["uid"] = rand_uid()
        elif isinstance(obj, str):
            # substitute flags for column values
            obj = re.sub(self.FLAG, lambda m: str(data.get(m.group(1), m.group(0))), obj)

        return obj

    def build(self, data) -> Dict:
        self.reset()
        if isinstance(data, str):
            data = json.load(open(data, "r"))

        results = []
        for component in self.template:
            print(component)
            # append static component to doc
            if component["type"] != "from_data":
                results.append(component)
                continue
            # build component for each row in data
            for row in data:
                for sub_component in component["body"]:
                    results.append(self.sub_values(deepcopy(sub_component), row))
            
        for component in results:
            uid = rand_uid()
            self.doc["form"][uid] = component
            self.doc["order"].append(uid)

        return self.doc

    def to_file(self, f, indent=4) -> Any:
        json.dump(self.doc, open(f, "w"), indent=indent)

