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

from airflow.hooks.mssql_hook import MsSqlHook
from airflow import configuration
from airflow import models
from airflow.utils import db
from hovertools import command_line

from .hooklib.basehooktest import BaseHookTest

# This catches sys.exit() calls, which are called by the Click library.
# If this is not done, all nosetests fail.
sys.exit = lambda *x: None
TMP_REPO_DIR = 'tmp'


class MsSqlHookTest(BaseHookTest):
    def __init__(self, *args, **kwargs):
        super(MsSqlHookTest, self).__init__('hooktests/hooks/specs/mssql.yaml',
                                            *args,
                                            **kwargs)

    def setUp(self):
        super(MsSqlHookTest, self).setUp()
        command_line.cli(['--repo', TMP_REPO_DIR, 'refresh', 'mssql_hook_test'])

        configuration.load_test_config()
        db.merge_conn(
                models.Connection(
                        conn_id='mssql_hook_test', conn_type='mssql',
                        host='localhost', port=1433, login='SA',
                        password=u'secret123_', schema='master'))
        self.db_hook = MsSqlHook(mssql_conn_id='mssql_hook_test', schema='master')

    def tearDown(self):
        pass

    def test_records(self):
        statement = "select * from master.dbo.sysprocesses"
        rows = self.db_hook.get_records(statement)
