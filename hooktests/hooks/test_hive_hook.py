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

from airflow.hooks.hive_hooks import HiveServer2Hook
from airflow import configuration
from airflow import models
from airflow.utils import db
from hovertools import command_line

from .hooklib.basehooktest import BaseHookTest

# This catches sys.exit() calls, which are called by the Click library.
# If this is not done, all nosetests fail.
sys.exit = lambda *x: None
TMP_REPO_DIR = 'tmp'


class HiveHookTest(BaseHookTest):
    def __init__(self, *args, **kwargs):
        super(HiveHookTest, self).__init__('hooktests/hooks/specs/hive.yaml',
                                            *args,
                                            **kwargs)

    def setUp(self):
        super(HiveHookTest, self).setUp()
        command_line.cli(['--repo', TMP_REPO_DIR, 'refresh', 'hive_hook_test'])

        configuration.load_test_config()
        db.merge_conn(
                models.Connection(
                        conn_id='hive_hook_test', conn_type='hiveserver2',
                        host='localhost', schema='default', port=10000,
                        login='username', password='password'))

        self.db_hook = HiveServer2Hook(hiveserver2_conn_id='hive_hook_test')

    def tearDown(self):
        pass

    def test_records(self):
        statement = "SELECT * FROM baby_names"
        rows = self.db_hook.get_records(statement)
