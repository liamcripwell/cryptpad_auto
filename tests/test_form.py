import json
import random

import pytest
import pandas as pd

from cryptpad_auto.forms import FormBuilder

@pytest.fixture
def basic_data():
    return json.load(open("tests/fixtures/basic_data.json", "r"))

@pytest.fixture
def basic_df():
    return pd.read_csv("tests/fixtures/basic_data.csv")

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

def test_basic_df_form_gen(basic_df, basic_temp, basic_form):
    builder = FormBuilder(basic_temp)
    result = builder.build(basic_df)
    
    assert result == basic_form