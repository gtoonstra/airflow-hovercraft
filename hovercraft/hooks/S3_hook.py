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

import smbc
import os
import logging

from airflow.hooks.S3_hook import S3Hook
from airflow.exceptions import AirflowException

import boto
from boto.s3.connection import S3Connection, NoHostProvided, OrdinaryCallingFormat
from boto.sts import STSConnection
boto.set_stream_logger('boto')
logging.getLogger("boto").setLevel(logging.INFO)


class HoverS3Hook(S3Hook):
    '''
    Interacts with S3 services
    '''
    def __init__(
            self,
            s3_conn_id='s3_default',
            *args, **kwargs):
        self.s3_conn_id = s3_conn_id
        self.s3_conn = self.get_connection(s3_conn_id)
        self.extra_params = self.s3_conn.extra_dejson
        self.profile = self.extra_params.get('profile')
        self.calling_format = None
        self.s3_host = None
        self.s3_port = None
        self.is_secure = True
        if 'port' in self.extra_params:
            self.s3_port = self.extra_params['port']
        if 'secure' in self.extra_params:
            self.is_secure = self.extra_params['secure']

        self._creds_in_conn = 'aws_secret_access_key' in self.extra_params
        self._creds_in_config_file = 's3_config_file' in self.extra_params
        self._default_to_boto = False
        if 'host' in self.extra_params:
            self.s3_host = self.extra_params['host']
        if self._creds_in_conn:
            self._a_key = self.extra_params['aws_access_key_id']
            self._s_key = self.extra_params['aws_secret_access_key']
            if 'calling_format' in self.extra_params:
                self.calling_format = self.extra_params['calling_format']
        elif self._creds_in_config_file:
            self.s3_config_file = self.extra_params['s3_config_file']
            # The format can be None and will default to boto in the parser
            self.s3_config_format = self.extra_params.get('s3_config_format')
        else:
            self._default_to_boto = True
        # STS support for cross account resource access
        self._sts_conn_required = ('aws_account_id' in self.extra_params or
                                   'role_arn' in self.extra_params)
        if self._sts_conn_required:
            self.role_arn = (self.extra_params.get('role_arn') or
                             "arn:aws:iam::" +
                             self.extra_params['aws_account_id'] +
                             ":role/" +
                             self.extra_params['aws_iam_role'])
        self.connection = self.get_conn()

    def get_conn(self):
        """
        Returns the boto S3Connection object.
        """
        if self._default_to_boto:
            return S3Connection(profile_name=self.profile)
        a_key = s_key = None
        if self._creds_in_config_file:
            a_key, s_key, calling_format = _parse_s3_config(self.s3_config_file,
                                                self.s3_config_format,
                                                self.profile)
        elif self._creds_in_conn:
            a_key = self._a_key
            s_key = self._s_key
            calling_format = self.calling_format
            s3_host = self.s3_host

        if calling_format is None:
            calling_format = 'boto.s3.connection.SubdomainCallingFormat'

        if s3_host is None:
            s3_host = NoHostProvided

        if self._sts_conn_required:
            sts_connection = STSConnection(aws_access_key_id=a_key,
                                           aws_secret_access_key=s_key,
                                           profile_name=self.profile)
            assumed_role_object = sts_connection.assume_role(
                role_arn=self.role_arn,
                role_session_name="Airflow_" + self.s3_conn_id
                )
            creds = assumed_role_object.credentials
            connection = S3Connection(
                aws_access_key_id=creds.access_key,
                aws_secret_access_key=creds.secret_key,
                calling_format=calling_format,
                security_token=creds.session_token
                )
        else:
            connection = S3Connection(aws_access_key_id=a_key,
                                      aws_secret_access_key=s_key,
                                      calling_format=calling_format,
                                      host=s3_host,
                                      port=self.s3_port,
                                      is_secure=False,
                                      profile_name=self.profile)
        return connection