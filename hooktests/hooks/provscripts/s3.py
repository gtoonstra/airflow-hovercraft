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

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key


parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host',
                    help='host ip',
                    required=True,
                    default='127.0.0.1')
parser.add_argument('-p', '--port', type=int,
                    help="S3 port to connect to",
                    default=4569)
parser.add_argument('-U', '--user',
                    help='username',
                    required=False,
                    default='ignored')
parser.add_argument('-P', '--password',
                    help='password',
                    required=False,
                    default='secret')
parser.add_argument('-D', '--database',
                    help='database name',
                    required=False,
                    default='default')
parser.add_argument('-c', '--container',
                    help='container id',
                    required=True,
                    default='default')
args = parser.parse_args()

print("Now connecting to S3")

access_key_id = 'ignored'
secret_access_key = 'ignored'
s3conn = S3Connection(access_key_id, secret_access_key, is_secure=False, port=args.port, host=args.host, calling_format=OrdinaryCallingFormat())

bucket = s3conn.create_bucket('mybucket')
k = Key(bucket)
k.key = 'foobar'
k.set_contents_from_string('This is a test of S3')
