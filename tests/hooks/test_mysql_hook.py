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

from hovercraft.hooks.mysql_hook import HCMySqlHook


class TestHCMySqlHook(unittest.TestCase):
    def setUp(self):
        super(TestHCMySqlHook, self).setUp()

        self.db_hook = HCMySqlHook(mysql_conn_id='mysql_default',
            schema='airflow_ci')

    def test_get_records(self):
        statement = "SELECT * FROM baby_names WHERE baby_name = 'Earl'"

        rows = ((1880, "Earl", 0.002829, "boy"),)

        self.assertEqual(rows, self.db_hook.get_records(statement))

    def test_calls(self):
        cur = mock.MagicMock()
        conn = mock.MagicMock()
        conn.cursor.return_value = cur
        
        class InstrumentedHook(HCMySqlHook):
            conn_name_attr = 'mysql_default'

            def get_conn(self):
                return conn

        db_hook = InstrumentedHook()

        statement = "SELECT * FROM baby_names WHERE baby_name = 'Earl'"
        rows = ((1880, "Earl", 0.002829, "boy"),)
        cur.fetchall.return_value = rows

        self.assertEqual(rows, db_hook.get_records(statement))

        conn.close.assert_called_once()
        cur.close.assert_called_once()
        cur.execute.assert_called_once_with(statement)