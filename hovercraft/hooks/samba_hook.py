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

from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException


class SambaHook(BaseHook):
    '''
    Allows for interaction with an samba server.
    '''

    def __init__(self, samba_conn_id):
        self.conn = self.get_connection(samba_conn_id)

    def get_conn(self):
        cb = lambda se, sh, w, u, p: (w, self.conn.login, self.conn.password)
        ctx = smbc.Context(auth_fn=cb)
        ctx.optionNoAutoAnonymousLogin = True
        ctx.timeout = 60000
        return ctx

    def push_from_local(self, destination_filepath, local_filepath):
        ctx = self.get_conn()

        filepath = "smb://{0}/{1}/{2}".format(
            self.conn.host, 
            self.conn.schema, 
            destination_filepath)
        folder = os.path.dirname(filepath)
        print(folder)
        try:
            st = ctx.stat(folder)
        except smbc.NoEntryError:
            print("Creating directory {0}".format(folder))
            ret = ctx.mkdir(folder, 0)
            if ret != 0:
                raise AirflowException(
                    "Could not create remote samba directory {0}"
                    .format(folder))

        print(filepath)
        sfile = open(local_filepath, 'rb')
        dfile = ctx.open(filepath, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
        for buf in sfile:
            ret = dfile.write(buf)
            if ret < 0:
                raise AirflowException("smbc write error")
        sfile.close()
        dfile.close()
