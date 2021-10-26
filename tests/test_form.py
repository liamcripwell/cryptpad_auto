import json
import random

import pytest

from cryptpad_auto.forms import FormBuilder

@pytest.fixture
def basic_data():
    return json.load(open("tests/fixtures/basic_data.json", "r"))

@pytest.fixture
def basic_temp():
    return json.load(open("tests/fixtures/basic_template.json", "r"))

@pytest.fixture
def basic_form():
    return json.load(open("tests/fixtures/basic_form.json", "r"))

def setup_function():
    random.seed(1) # needed to match fixture uids

def test_basic_form_gen(basic_data, basic_temp, basic_form):
    builder = FormBuilder(basic_temp)
    result = builder.build(basic_data)
    
    assert result == basic_form