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

import logging
from ftplib import FTP_TLS
from airflow.contrib.hooks.ftp_hook import FTPHook


class FTPSHook(FTPHook):

    def get_conn(self):
        """
        Returns a FTPS connection object.
        """
        if self.conn is None:
            params = self.get_connection(self.ftp_conn_id)

            self.conn = FTP_TLS(timeout=60)
            self.conn.connect(params.host, params.port)
            self.conn.auth()
            self.conn.prot_p()
            self.conn.login(params.login, params.password)

        return self.conn
