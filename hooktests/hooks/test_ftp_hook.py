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
from io import BytesIO

from hovercraft.hooks.ftp_hook import FTPSHook
from airflow import configuration
from airflow import models
from airflow.utils import db
from hovertools import command_line

from .hooklib.basehooktest import BaseHookTest

# This catches sys.exit() calls, which are called by the Click library.
# If this is not done, all nosetests fail.
sys.exit = lambda *x: None
TMP_REPO_DIR = 'tmp'


class FTPSHookTest(BaseHookTest):
    def __init__(self, *args, **kwargs):
        super(FTPSHookTest, self).__init__('hooktests/hooks/specs/ftps.yaml',
                                         *args,
                                         **kwargs)

    def setUp(self):
        super(FTPSHookTest, self).setUp()
        command_line.cli(['--repo', TMP_REPO_DIR, 'refresh', 'ftps_hook_test'])

        configuration.load_test_config()
        db.merge_conn(
                models.Connection(
                    conn_id='ftps_hook_test', conn_type='ftp',
                    host='172.17.0.1', port=2221, 
                    login='foo', password='123'))

        self.hook = FTPSHook(ftp_conn_id='ftps_hook_test')

    def tearDown(self):
        pass

    def test_records(self):
        local_path = BytesIO()
        self.hook.retrieve_file(remote_full_path='test.txt', local_full_path_or_buffer=local_path)
        local_path.seek(0)
        print(local_path.getvalue())
        assert local_path.getvalue() == b'this is a test file\n'
