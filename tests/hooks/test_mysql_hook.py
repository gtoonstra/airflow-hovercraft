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

import sys

from airflow.hooks.mysql_hook import MySqlHook
from airflow import configuration
from airflow import models
from airflow.utils import db
from hovertools import command_line

from .hooklib.basehooktest import BaseHookTest

# This catches sys.exit() calls, which are called by the Click library.
# If this is not done, all nosetests fail.
sys.exit = lambda *x: None
TMP_REPO_DIR = 'tmp'


class MySqlHookTest(BaseHookTest):
    def __init__(self, *args, **kwargs):
        super(MySqlHookTest, self).__init__('tests/hooks/specs/mysql.yaml',
                                            *args,
                                            **kwargs)

    def setUp(self):
        super(MySqlHookTest, self).setUp()
        command_line.cli(['--repo', TMP_REPO_DIR, 'refresh', 'mysql_hook_test'])

        configuration.load_test_config()
        db.merge_conn(
                models.Connection(
                        conn_id='mysql_hook_test', conn_type='mysql',
                        host='127.0.0.1', port=6604, login='root',
                        password='secret', schema='mysql'))
        self.db_hook = MySqlHook(mysql_conn_id='mysql_hook_test', schema='mysql')

    def tearDown(self):
        pass

    def test_records(self):
        statement = "SELECT * FROM user"
        rows = self.db_hook.get_records(statement)
        print(rows)
        assert False
