#!/usr/bin/env python

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
