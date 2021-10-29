# cryptpad_auto

This project contains automation tools for CryptPad documents. It provides a templating interface that can be used to generate forms for a given datset. For example, if you had a large set of questions and wanted to generate a form containing a component for each entry.

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

## Generating Forms
### Form Templates

Forms are generating based on a template provided by the user. The accepted format is similar to the JSON used by CryptPad, but with a few modifications. 
* It should take the form of an ordered list of JSON objects specifying each component to be included in the form.
* The special `from_data` component type should be used to specify parts of the form that should be created for each item in a dataset.
* Column or attribute values of the item can by referenced in any text value by placing them between `$` characters (e.g. `"Question: $column_name$"`).

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
