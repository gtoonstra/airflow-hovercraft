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

from hovercraft.hooks.S3_hook import HoverS3Hook
from airflow import configuration
from airflow import models
from airflow.utils import db
from hovertools import command_line

from .hooklib.basehooktest import BaseHookTest

# This catches sys.exit() calls, which are called by the Click library.
# If this is not done, all nosetests fail.
sys.exit = lambda *x: None
TMP_REPO_DIR = 'tmp'


class S3HookTest(BaseHookTest):
    def __init__(self, *args, **kwargs):
        super(S3HookTest, self).__init__('hooktests/hooks/specs/s3.yaml',
                                         *args,
                                         **kwargs)

    def setUp(self):
        super(S3HookTest, self).setUp()
        command_line.cli(['--repo', TMP_REPO_DIR, 'refresh', 's3_hook_test'])

        configuration.load_test_config()
        db.merge_conn(
                models.Connection(
                    conn_id='s3_hook_test', conn_type='s3',
                    extra='{"aws_access_key_id":"_your_aws_access_key_id_",\
                        "aws_secret_access_key":"_your_aws_secret_access_key_",\
                        "host":"localhost",\
                        "port": 4569,\
                        "secure": false}'))

        self.hook = HoverS3Hook(s3_conn_id='s3_hook_test')

    def tearDown(self):
        pass

    def test_records(self):
        s3_key = 'foobar'
        if not self.hook.check_for_key(s3_key, bucket_name='mybucket'):
            raise Exception("The source key {0} does not exist"
                            "".format(s3_key))
        source_s3_key_object = self.hook.get_key(s3_key, bucket_name='mybucket')
        assert source_s3_key_object.get_contents_as_string() == b"This is a test of S3"
