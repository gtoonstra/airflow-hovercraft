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

from airflow.hooks.base_hook import BaseHook


class FakeTrueHook(object):
    def get_first(self, sql, parameters=None):
        return (True,)


class FakeFalseHook(object):
    def get_first(self, sql, parameters=None):
        return (False,)


class FakeMultiTrueHook(object):
    def get_first(self, sql, parameters=None):
        return (True,True,True,)


class FakeMultiTrueOneFalseHook(object):
    def get_first(self, sql, parameters=None):
        return (True,True,False,)


class FakeNoneHook(object):
    def get_first(self, sql, parameters=None):
        return None


class Fake42Hook(object):
    def get_first(self, sql, parameters=None):
        return (42.0,)
