#!/bin/bash
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

# This script provisions a MySQL docker instance

OPTIND=1

# Initialize our own variables:
host=""
user=""
secret=""
port=""

while getopts "h:u:s:p:" opt; do
    case "$opt" in
    h)  host=$OPTARG
        ;;
    u)  user=$OPTARG
        ;;
    s)  secret=$OPTARG
        ;;
    p)  port=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

echo "Provisioning host='$host' with user='$user' at port='$port'"

function fail {
    echo $1
    exit
}

mysql -u $user -P $port -p$secret -h $host -e 'create database test' || fail "Could not create database"
