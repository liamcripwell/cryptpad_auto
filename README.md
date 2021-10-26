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

Forms are generating based on a template provided by the user. The accepted format is similar to the JSON used by CryptPad, but excludes some information like `uid` fields. It should take the form of an ordered list of JSON objects specifying each component to be included in the form.

The special `from_data` component type should be used to generate a part of the template for each item in the dataset. Column or attribute values of the item can by referenced in any text value by placing them between `$`s (e.g. `$column_name$`)

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
        "type": "multiradio",
        "q": "Question $i$",
        "opts": {
          "items": [
            {
              "v": "$col1$"
            }
          ],
          "values": [
            {
              "v": "True"
            },
            {
              "v": "False"
            }
          ]
          "required": true
        }
      }
    ]
  }
]
```
