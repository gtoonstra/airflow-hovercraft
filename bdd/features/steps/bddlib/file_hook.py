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

import pandas as pd


class Cursor(object):
    def execute(self, sql, parameters=None):
        self.df = pd.read_csv(sql)
        self.description = self.df.columns
        self.high = len(self.df)
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.df.iloc[self.current-1]

    def close(self):
        self.df = None
        del self.df


class Conn(object):
    def __init__(self, *args, **kwargs):
        self.crsr = Cursor()

    def cursor(self):
        return self.crsr

    def close(self):
        self.crsr = None
        del self.crsr


class FileHook(object):
    def __init__(self, *args, **kwargs):
        self.conn = Conn()
        self.cursor = self.conn.cursor()

    def run(self, sql, autocommit=False, parameters=None):
        pass

    def get_conn(self):
        return self.conn

    def load_file(
            self,
            filepath,
            table,
            delimiter=",",
            field_dict=None,
            create=True,
            overwrite=True,
            partition=None,
            recreate=False):
        print(filepath)
