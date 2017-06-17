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
container=""

while getopts "h:u:s:p:c:" opt; do
    case "$opt" in
    h)  host=$OPTARG
        ;;
    u)  user=$OPTARG
        ;;
    s)  secret=$OPTARG
        ;;
    p)  port=$OPTARG
        ;;
    c)  container=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

echo "Provisioning host='$host' with user='$user' at port='$port', container='$container'"

function fail {
    echo $1
    exit
}

export CONTAINER=$container

docker exec -ti ${CONTAINER} /bin/bash -c "mkdir /home/example1 && \
            mkdir /home/example2 && \
            mkdir /home/public && exit"

docker exec -ti ${CONTAINER} /bin/bash -c "/usr/bin/samba.sh -u \"example1;badpass\" \
            -u \"example2;badpass\" \
            -s \"public;/home/public\" \
            -s \"users;/srv;no;no;no;example1,example2\" \
            -s \"example1 private;/home/example1;no;no;no;example1\" \
            -s \"example2 private;/home/example2;no;no;no;example2\" \
 && exit"

docker restart ${CONTAINER}
