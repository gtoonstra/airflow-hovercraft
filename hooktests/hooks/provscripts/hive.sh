#!/bin/bash

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
docker cp hooktests/hooks/data/baby_names.csv ${CONTAINER}:/home/cloudera/baby_names.csv

docker exec -ti ${CONTAINER} /bin/bash -c "beeline << EOF
!connect jdbc:hive2://localhost:10000 hive hive
create table baby_names(
    year STRING,
    name STRING,
    percent FLOAT,
    sex  STRING
);
load data local inpath '/home/cloudera/baby_names.csv' into table baby_names;
EOF
exit"

# Do some hive stuff here...
# create table t1 (s string);