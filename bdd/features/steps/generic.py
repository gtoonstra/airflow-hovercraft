# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import importlib
import ast
from unittest.mock import patch
from bddlib.fake_hook import FakeHook
from airflow.hooks.base_hook import BaseHook


def get_default_context():
    return {}


@given('no specific state')
def step_impl(context):
    pass


@given('a specific initializer')
def step_impl(context):
    if context.table is not None:
        row = context.table[0]
        headers = context.table.headings
        d = {}
        for header in headers:
            d[header] = ast.literal_eval(row[header])
        context.initializer = d


@given('hook mocked with FakeHook')
def step_impl(context):
    returned_data = {}
    if context.table is not None:
        row = context.table[0]
        headers = context.table.headings
        for header in headers:
            returned_data[header] = ast.literal_eval(row[header])

    def get_hook(conn_id='fake'):
        return FakeHook(returned_data)
    BaseHook.get_hook = get_hook


@when('the {operator_type} is created')
def step_impl(context, operator_type):
    """
    This step checks if it can instantiate
    a class of a certain type
    """
    try:
        context.exception = None
        s = operator_type.split(".")
        mod = ".".join(s[:len(s)-1])
        clz = s[len(s)-1]
        MyClass = getattr(importlib.import_module(mod), clz)
        
        d = {}
        if "initializer" in context:
            d = context.initializer
            d['task_id'] = 'test'
            context.instance = MyClass(**d)
        else:
            context.instance = MyClass(task_id='test')
    except Exception as e:
        context.exception = e


@then('the operator is executed')
def step_impl(context):
    try:
        ctxt = get_default_context()
        context.return_value = context.instance.execute(ctxt)
    except Exception as e:
        context.exception = e


@then('no exception is raised')
def step_impl(context):
    """
    This step just checks if an exception was raised
    in a previous step.
    """
    if context.exception is not None:
        raise context.exception


@then('the exception {exception_type} is raised')
def step_impl(context, exception_type):
    """
    This step just checks if an exception was raised
    in a previous step.
    """
    if context.exception is None:
        raise Exception("No exception was raised when one was expected")

    assert type(context.exception).__name__ == exception_type


@then('the return value is {return_value}')
def step_impl(context, return_value):
    """
    This step just checks if an exception was raised
    in a previous step.
    """
    if context.return_value is not None:
        assert str(context.return_value) == str(return_value)
    else:
        raise Exception("No return value from operator")
