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


@given('no specific state')
def step_impl(context):
    pass


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
        instance = MyClass(task_id='test')
    except Exception as e:
        context.exception = e


@then('it does not raise an exception')
def step_impl(context):
    """
    This step just checks if an exception was raised
    in a previous step.
    """
    if context.exception is not None:
        raise context.exception
