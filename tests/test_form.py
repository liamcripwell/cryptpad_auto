import json
import random

import pytest
import pandas as pd

from cryptpad_auto.forms import FormBuilder, FormTemplateBuilder

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
def all_temp():
    return json.load(open("tests/fixtures/all_comp_temp.json", "r"))

@pytest.fixture
def all_temp_uids():
    return json.load(open("tests/fixtures/all_comp_temp_uids.json", "r"))

@pytest.fixture
def basic_form():
    return json.load(open("tests/fixtures/basic_form.json", "r"))

@pytest.fixture
def all_form():
    return json.load(open("tests/fixtures/all_comp_form.json", "r"))


def setup_function():
    random.seed(1) # needed to match fixture uids

def test_basic_form_gen(basic_data, basic_temp, basic_form):
    builder = FormBuilder(basic_temp)
    result = builder.build(basic_data)
    
    assert result == basic_form

def test_basic_form_gen_from_file(basic_temp, basic_form):
    builder = FormBuilder(basic_temp)
    result = builder.build("tests/fixtures/basic_data.json")
    
    assert result == basic_form

def test_basic_df_form_gen(basic_df, basic_temp, basic_form):
    builder = FormBuilder(basic_temp)
    result = builder.build(basic_df)
    
    assert result == basic_form

def test_basic_df_form_gen_from_file(basic_temp, basic_form):
    builder = FormBuilder(basic_temp)
    result = builder.build("tests/fixtures/basic_data.csv")
    
    assert result == basic_form

def test_all_comp_no_data(all_temp, all_form):
    builder = FormBuilder(all_temp)
    result = builder.build([])
    
    assert result == all_form

def test_all_comp_no_data(all_temp_uids, all_form):
    builder = FormBuilder(all_temp_uids)
    result = builder.build([])
    
    assert result == all_form

def test_template_conversion(all_temp, all_form):
    builder = FormBuilder(None)
    tbuilder = FormTemplateBuilder(all_form)
    builder.template = tbuilder.build()
    result = builder.build([])

    assert builder.template == all_temp
    assert result == all_form