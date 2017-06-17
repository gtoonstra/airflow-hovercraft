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

from airflow.hooks.samba_hook import SambaHook
from airflow import configuration
from airflow import models
from airflow.utils import db
from hovertools import command_line

from .hooklib.basehooktest import BaseHookTest

# This catches sys.exit() calls, which are called by the Click library.
# If this is not done, all nosetests fail.
sys.exit = lambda *x: None
TMP_REPO_DIR = 'tmp'


class SambaHookTest(BaseHookTest):
    def __init__(self, *args, **kwargs):
        super(SambaHookTest, self).__init__('hooktests/hooks/specs/samba.yaml',
                                            *args,
                                            **kwargs)

    def setUp(self):
        super(SambaHookTest, self).setUp()
        command_line.cli(['--repo', TMP_REPO_DIR, 'refresh', 'samba_hook_test'])

        configuration.load_test_config()
        db.merge_conn(
                models.Connection(
                        conn_id='samba_hook_test', conn_type='samba',
                        host='localhost', login='example1',
                        password='badpass', schema='public'))
        self.samba_hook = SambaHook(samba_conn_id='samba_hook_test')

    def tearDown(self):
        pass

    def test_share(self):
        local_dir = os.path.basename(__file__)
        datafile = os.path.join(local_dir, 'data', 'daily_report.csv')
        rows = self.samba_hook.push_from_local('daily_report.csv', datafile)
