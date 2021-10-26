import json
import random

import pytest

from cryptpad_generation.generate import generate_form

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
    result = generate_form(basic_data, basic_temp)
    
    assert result == basic_form