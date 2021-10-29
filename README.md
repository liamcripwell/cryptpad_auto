# cryptpad_auto

This project contains automation tools for [CryptPad](https://github.com/xwiki-labs/cryptpad) documents. It provides a templating interface that can be used to generate forms for a given datset. For example, if you had a large set of questions and wanted to generate a form containing a component (or set of components) for each entry.

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Tests

We provide some unit tests to confirm whether the tool is functioning with your system.

```bash
pytest tests
```

## Forms
### Form Templates

Forms are generated according to a template provided by the user. The accepted format is similar to the JSON used by CryptPad, but with a few modifications. 
* It should take the form of an ordered list of JSON objects specifying each component to be included in the form.
* The special `from_data` component type should be used to wrap parts of the form that should be created for each item in a dataset.
* Column or attribute values of the dataset item can by referenced within any text value between `$` flags (e.g. `"Question: $column_name$"`).

For example, the follow template will produce a form with a number input field for each row in the data:
```json
[
  {
    "type": "md",
    "opts": {
      "text": "This is the initial description of the form."
    }
  },
  {
    "type": "from_data",
    "body": [
      {
        "type": "input",
        "q": "How many $col1$?",
        "opts": {
          "type": "number"
        }
      }
    ]
  }
]
```

You can quickly generate a template from an existing exported form via the terminal (Note: `$` flags currently need to be manually inserted):
```bash
# will not include any `from_data` structures
python run.py template --form_file=exported_form.json --out_file=template.json

# will wrap the 2nd and 3rd components in a `from_data` structure
python run.py template --form_file=exported_form.json --out_file=template.json --data_groups="[[1,2]]"
```

### Generating Forms
Forms are generated via the `FormGenerator` class. The template and data can be passed either as filenames or appropriate python data structures. 
```python
from cryptpad_auto.forms import FormBuilder

builder = FormBuilder("template_file.json") # can also provide a `dict` template

form = builder.build("some_data.csv") # can also be a `.json` file, `list[dict]` or `pandas.DataFrame` object

builder.to_file("new_form.json")
```

Alternatively, you can generate a form directly via the terminal:
```bash
python run.py form --template_file=template.json --data_file=data.csv --out_file=form.json
```
