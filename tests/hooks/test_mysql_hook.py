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
#

import mock
import unittest

from airflow.hooks.dbapi_hook import DbApiHook


class TestMySqlHook(unittest.TestCase):
    def setUp(self):
        super(TestMySqlHook, self).setUp()

        self.cur = mock.MagicMock()
        self.conn = conn = mock.MagicMock()
        self.conn.cursor.return_value = self.cur

        class HCMysqlHook(DbApiHook):
            conn_name_attr = 'test_conn_id'
            
            def get_conn(self):
                return conn

        self.db_hook = HCMysqlHook()

    def test_get_records(self):
        statement = "SQL"
        rows = [("hello",),
                ("world",)]

        self.cur.fetchall.return_value = rows

        self.assertEqual(rows, self.db_hook.get_records(statement))

        self.conn.close.assert_called_once()
        self.cur.close.assert_called_once()
        self.cur.execute.assert_called_once_with(statement)
