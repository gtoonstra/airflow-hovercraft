#!/usr/bin/env python

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

import argparse

import pymssql

parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host',
                    help='host ip',
                    required='True',
                    default='127.0.0.1')
parser.add_argument('-p', '--port', type=int,
                    help="DB port to connect to",
                    default=1433)
parser.add_argument('-U', '--user',
                    help='username',
                    required='True',
                    default='sa')
parser.add_argument('-P', '--password',
                    help='password',
                    required='True',
                    default='secret')
parser.add_argument('-D', '--database',
                    help='database name',
                    required='True',
                    default='default')
args = parser.parse_args()

print("Now connecting to SQL Server")

conn = pymssql.connect(server=args.host, 
                       user=args.user,
                       password=args.password,
                       port=args.port,
                       database=args.database)
