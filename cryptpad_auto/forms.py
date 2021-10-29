import re
import json
from copy import deepcopy
from typing import Any, Dict, List

from cryptpad_auto.utils import *


class FormBuilder():

    FLAG = r'\$([a-zA-z0-9]+)\$'

    def __init__(self, template=None) -> None:
        self.template = read_data_file(template)
        self.reset()

    def reset(self) -> None:
        self.used_uids = []
        self.doc = {
            "form": {},
            "order": [],
            "version": 1
        }

    def sub_values(self, obj: Any, data=None) -> Any:
        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = self.sub_values(obj[i], data)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self.sub_values(value, data)
            # add a uid to the object if needed
            if needs_uid(obj):
                obj["uid"] = rand_uid(self.used_uids)
                self.used_uids.append(obj["uid"])
        elif isinstance(obj, str) and data is not None:
            # substitute flags for column values
            obj = re.sub(self.FLAG, lambda m: str(data.get(m.group(1), m.group(0))), obj)

        return obj

    def build(self, data: Any) -> Dict:
        if self.template is None:
            raise ValueError("Cannot build form when no template has been provided.")

        self.reset()

        # prepare data and iterator
        data = read_data_file(data)
        data_iter = get_data_iterator(data)

        results = []
        for component in self.template:
            # append static component to doc
            if component["type"] != "from_data":
                results.append(self.sub_values(deepcopy(component)))
                continue
            # build component for each row in data
            for _, row in data_iter:
                for sub_component in component["body"]:
                    results.append(self.sub_values(deepcopy(sub_component), row))
            
        # build final form document structure
        for component in results:
            uid = rand_uid(self.used_uids)
            self.used_uids.append(uid)
            self.doc["form"][uid] = component
            self.doc["order"].append(uid)

        return self.doc

    def to_file(self, f: str, indent=4) -> None:
        json.dump(self.doc, open(f, "w"), indent=indent)


class FormTemplateBuilder():

    def __init__(self, form):
        self.reset()
        self.form = read_data_file(form)

    def reset(self) -> None:
        self.template = []

    def build(self, data_groups=[]) -> List:
        self.reset()

        components = list(self.form["form"].values())
        for g in data_groups:
            group = []
            for i in range(len(components)):
                if i in g:
                    group.append(components[i])
            components[g[0]] = group
            for i in g[1:]:
                components.pop(i)

        for c in components:
            if isinstance(c, list):
                sub_cs = [strip_key_r(deepcopy(_c), "uid") for _c in c]
                self.template.append(self.data_wrap(sub_cs))
            else:
                clean_c = strip_key_r(deepcopy(c), "uid")
                self.template.append(clean_c)

        return self.template

    def to_file(self, f: str, indent=4) -> None:
        json.dump(self.template, open(f, "w"), indent=indent)

    def data_wrap(self, components: List) -> Dict:
        return {
            "type": "from_data",
            "body": components
        }